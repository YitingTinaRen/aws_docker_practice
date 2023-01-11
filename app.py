from flask import *
import mysql.connector
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from werkzeug.utils import secure_filename
import config

app=Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/pic", methods=["POST"])
def pic():
    if request.method =="POST":
        file=request.files["file"]
        msg=request.form["content"]
        file.filename = secure_filename(file.filename)
        if file.filename and msg:
            # create unique key
            now = datetime.now()
            key = datetime.strftime(now, '%Y%m%d%H%M%S%f')
            # Save file to s3 with the unique key
            s3=boto3.client(
                "s3",
                aws_access_key_id=config.S3_KEY_ID,
                aws_secret_access_key=config.S3_SECRET_KEY)
            try:
                s3.upload_fileobj(
                    file,
                    'pickprice', 
                    key,
                    ExtraArgs={
                        "ACL":"public-read",
                        "ContentType":file.content_type
                    })
            except ClientError as e:
                print(e)
                return False

            # Save the msg and key information into RDS
            mydb=mysql.connector.connect(pool_name=config.DB_POOL_NAME)
            mycursor=mydb.cursor()
            sql="insert into HW (msg , pic_key) values (%s, %s)"
            val=(msg, key)
            mycursor.execute(sql,val)
            mydb.commit()
            mycursor.close()
            mydb.close()

            myresult=[msg, config.CLOUDFRONT+key]

            return myresult
        else:
            print("No file or msg!")
            return jsonify({"error":True, "message":"Not proper inputs."}), 400

@app.route("/api/history", methods=["GET"])
def history():
    # Obtain history data order by date asc
    sql="select msg, pic_key from HW order by time desc"
    val=()
    mydb = mysql.connector.connect(pool_name=config.DB_POOL_NAME)
    mycursor = mydb.cursor()
    mycursor.execute(sql,val)
    myresult=mycursor.fetchall()
    mycursor.close()
    mydb.close()

    for i in range( len(myresult)):
        myresult[i]=list(myresult[i])
        myresult[i][1]=config.CLOUDFRONT+myresult[i][1]
        myresult[i] = tuple(myresult[i])
    
    return myresult





if __name__=="__main__":
    dbconfig={
        "host": config.DB_HOST,
        "port":config.DB_PORT,
        "user":config.DB_USER,
        "password":config.DB_PASSWORD,
        "database":config.DB_DB
    }
    mydb=mysql.connector.connect(
        pool_name=config.DB_POOL_NAME,
        pool_size=config.DB_POOL_SIZE,
        **dbconfig
    )
    mydb.close()
    app.run(port=config.PORT, debug=config.DEBUG)