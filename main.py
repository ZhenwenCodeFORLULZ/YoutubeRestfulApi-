from flask import Flask, request
from flask_restful import Api, Resource, reqparse,abort,fields,marshal_with
#marshal_with is a decroater
from flask_sqlalchemy import SQLAlchemy, Model


app = Flask(__name__) # used when you create a new flask app
api = Api(app)  # wrap our app inside a api
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    # defines all the fields we want in this model
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable = False) # nullable = False means that this field needs to have some information
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer,nullable = False)

    def __repr__(self):
        return f"Video(name={name},views = {views},likes={likes})"

#db.create_all() # call it once or else we will overide the columns and rows 
#db.create_all will make us a database with all these models within it

video_put_args = reqparse.RequestParser()
#help displays what we send to sender, basically an error message
video_put_args.add_argument("name", type = str, help = "Name of the Video",required = True)
# required = True crashes if invalid
video_put_args.add_argument("views", type = int, help = "Views of the Video",required = True)
video_put_args.add_argument("likes", type = int, help = "Likes of the Video",required = True)
# these three are the types of arguements needed for a argument parser

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type = str, help = "Name of the Video")
video_update_args.add_argument("name", type = int, help = "Views of the Video")
video_update_args.add_argument("name", type = int, help = "Likes of the Video")
# resource fields defines how objects should be serialized
resource_fields = {
    'id': fields.Integer, 
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
# a dictionary that defines the fields from the video model
}


class Video(Resource):
    @marshal_with(resource_fields) #creates {'id': id },# serializer
    def get(self,video_id):
        result = VideoModel.query.filter_by(id = video_id).first() # an instance of object video model
        if not result:
            abort(404,message = "Could not find video with that id")
        return result

    @marshal_with(resource_fields)
    def put(self,video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409,message = "Video id taken already...")
        video = VideoModel(id = video_id, name = args['name'],views = args['views'],likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201 # returns a specific status code 201 - created

    @marshal_with(resource_fields)
    def delete(self,video_id):
        abort_if_video_id_dosent_exist(video_id)
        del videos[video_id]
        return '', 204

    @marshal_with(resource_fields)
    def patch(self,video_id): # a way to update
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404,message = "Video dosent exist, cannot update")
        if  args['name']:
            result.name = args['name']
        if  args['views']:
            result.views = args['views']
        if  args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result
       

#making a new instance of the model

api.add_resource(Video, "/video/<int:video_id>") # <string> allows you to add string info into it


if __name__ == "__main__":
    app.run(debug= True) #debug = True, allows us to see logging info dont run in production



 