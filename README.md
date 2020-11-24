This application is used for compressing down the video by factor provided by the user of the original video file

I have deployed the model on heroku platform
You can run this on your local machine by using https://compress-api.herokuapp.com/
Required compressed file will be mailed on your specified google account

I have used openCV to do so

Folowing are the steps that i followed
1) extracted all the frames from a provided video file
2) Resized(Scale down) all the frames to given percentage of original size 
3) finally merged all the frames to a video again
