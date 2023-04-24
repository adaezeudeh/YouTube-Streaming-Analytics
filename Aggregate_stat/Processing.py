import pandas as pd
import psycopg2
import api_config
from flask import Flask, jsonify, request
import json

# Connect to the database
conn = psycopg2.connect(
    user=api_config.user,
    password=api_config.password,
    host=api_config.host,
    port=api_config.port,
    database=api_config.database
)

# Query the database and create a DataFrame
df = pd.read_sql_query("SELECT channel_title, views, likes FROM youtube_data", conn)

# Group the DataFrame by channel_title and calculate the aggregate statistics
grouped_df = df.groupby('channel_title').agg({
    'views': ['sum', 'mean'],
    'likes': ['sum', 'mean']
})

# Convert the DataFrame to a nested dictionary
grouped_dict = grouped_df.to_dict()

# Create Flask app
app = Flask(__name__)

# Define API endpoint for getting aggregated views by channel
@app.route('/views', methods=['GET'])
def get_views_by_channel():
    channel = request.args.get('channel')
    views_data = []
    for channel_title, values in grouped_dict[('views', 'sum')].items():
        if not channel or channel_title.lower() == channel.lower():
            views_sum = values
            views_mean = grouped_dict[('views', 'mean')][channel_title]
            views_data.append({
                'channel_title': channel_title,
                'views_sum': views_sum,
                'views_mean': views_mean
            })
    return jsonify({'views_data': views_data})

# Define API endpoint for getting aggregated likes by channel
@app.route('/likes', methods=['GET'])
def get_likes_by_channel():
    channel = request.args.get('channel')
    likes_data = []
    for channel_title, values in grouped_dict[('likes', 'sum')].items():
        if not channel or channel_title.lower() == channel.lower():
            likes_sum = values
            likes_mean = grouped_dict[('likes', 'mean')][channel_title]
            likes_data.append({
                'channel_title': channel_title,
                'likes_sum': likes_sum,
                'likes_mean': likes_mean
            })
    return jsonify({'likes_data': likes_data})

# Define API endpoint for getting individual records by video title
@app.route('/record', methods=['GET'])
def get_record_by_title():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Please provide a video title'})
    query = "SELECT * FROM youtube_data WHERE title ILIKE %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (f'%{title}%',))
        records = cursor.fetchall()
    if not records:
        return jsonify({'error': 'No records found for the given video title'})
    # Convert the result to a list of dictionaries
    video_record = []
    for record in records:
        record_dict = {
            'video_id': record[0],
            'title': record[2],
            'channel_title': record[3],
            'category_id': record[4],
            'views': record[7],
            'likes': record[8],
            'dislikes': record[9],
            'comment_count': record[10],
            'thumbnail_link': record[11],
            'date_published': record[5],
            'tags': record[6],
            'description': record[15]
        }
        video_record.append(record_dict)
    return jsonify({'video_record': video_record})


# Pretty print JSON output with indent
@app.after_request
def add_header(response):
    response.data = json.dumps(json.loads(response.data), indent=2)
    response.headers['Content-Type'] = 'application/json'
    return response

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000)
