from pymongo.errors import BulkWriteError

def create_collections_unique(db, video_names):
    videos_map = {}
    for video in video_names:
        video_collection = db[video]
        video_collection.delete_many({})
        video_collection.create_index("frame", unique=True)
        videos_map.update({video: []})
    return videos_map

def insert_data_unique(db, videos_map):
    for video, docs in videos_map.items():
        video_collection = db[video]
        # print(docs)
        try:
            _result = video_collection.insert_many(docs)
            # print('Multiple Documents have been inserted.')
            for doc_id in _result.inserted_ids:
                print(doc_id)
            print()
        except BulkWriteError:
            # print("Batch Contains Duplicate")
            for doc in docs:
                if video_collection.find_one({"frame": doc["frame"]}) != None:
                    continue
                # print("inserting one by one")
                video_collection.insert_one(doc)
        except Exception as e:
            print("Error Occured.")
            print(e)
            print(docs)
            pass