#importing different pakages
from flask import Flask,render_template,request,url_for,redirect
from flask_mail import Mail,Message 
from werkzeug.utils import secure_filename
import cv2
import os
# re module provides support 
# for regular expressions 
import re 
  
# Make a regular expression 
# for validating an Email 
regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"

#app configurations
app=Flask(__name__)
app.config['UPLOAD_FOLDER']= 'uploads/'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USERNAME']='aadarshgupta875@gmail.com'
app.config['MAIL_PASSWORD']='******'
app.config['MAIL_DEFAULT_SENDER']='aadarshgupta875@gmail.com'

mail=Mail(app)

@app.route('/',methods=["GET","POST"])
def start():
	return render_template('compress.html')

@app.route('/compress',methods=["POST"])
def compress():

	#loads file from html
	videoFile=request.files['filename']

	#retrieve scale down/up factor
	resize_frame=int(request.form.get("scale_factor"))

	#retrieves email ID from html
	recipient_id=str(request.form.get("email"))

	#if invalid email is provided 
	if not(re.search(regex,recipient_id)):
		return render_template("compress.html",text="Invalid Email Id")

	#contains filename
	fn=os.path.basename(videoFile.filename)

	#saving file in specified directory
	videoFile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(videoFile.filename)))

	#contains path where file is saved
	videoFile=os.path.join(app.config['UPLOAD_FOLDER'])+fn

	#dividing the file location into its filename and extension
	name, ext =os.path.splitext(videoFile)

	#checking whether the file is videofile or not 
	allowed_extensions=[".mp4" , ".mov" , ".avi" , ".webm" , ".wmv" , ".flv"]
	if (ext.lower() in allowed_extensions)==False:
		return render_template("compress.html",text="not a video file extension")

	#capturing the vedio
	cap=cv2.VideoCapture(videoFile)

	#output file name
	output_vedio_file="compressed_"+fn

	#making mp4 output vedio file
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')

	#Get frame per second of the vedio
	frame_per_second=cap.get(cv2.CAP_PROP_FPS)

	#get frame size
	width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	print(output_vedio_file)
	#scaling down/up the frame
	new_width=int(width*resize_frame/100)
	new_height=int(height*resize_frame/100)
	size=(new_width,new_height)

	#Initialize VedioWriter
	out = cv2.VideoWriter(output_vedio_file, fourcc , frame_per_second, size,True)

	while(1):
		ret, frame=cap.read()
		if ret==False:
			break
		resizeFrame=cv2.resize(frame,size)
		out.write(resizeFrame)

	cap.release()
	out.release()

	try:
		#Message Content that is to be emailed 
		msg=Message(
			subject='Compressed video file',
			recipients=[recipient_id],
			body='Below is your required Compressed video File'
			)

		#attaching gray scale video file
		with app.open_resource(output_vedio_file) as output_file:
			msg.attach(output_vedio_file,'video/mp4',output_file.read())

		#sending mail
		mail.send(msg)

		return render_template("compress.html",text="Successfully mailed the Compressed videofile to your provided email id")	

	except Exception:
		return render_template("compress.html",text="Sorry!!! Currently application is out of service")
		
if __name__=="__main__":
	app.run()
