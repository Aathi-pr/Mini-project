import json
import logging
import time

import openrouteservice
import requests
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from geopy.distance import geodesic

from TukTukGO import connectdb, currentDate


# Create your views here.
def homePage(request): #Home page of TukTukGo
    return render(request, "index.html")

def signUpPage(request): # Common SignUp page for Admin, Drivers, and Users
    return render(request, "signUp.html")

def validateLogin(request): # This function validates the login credentials and redirects to their page

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    userID = request.POST['userID']
    EMail = request.POST['EMail']
    password = request.POST['password']

    query = "SELECT * FROM loginCredentials WHERE UserID = '" + userID + "' and EMail = '" + EMail + "' and password = '" + password + "'"
    cursor.execute(query)

    if cursor.rowcount == 0:

        msg = "Invalid E-Mail or Password \n Please Try Again"

        return render(request, "signUp1.html", {
            'msg': msg
            })

    elif userID == "Admin":

        query = ("DELETE FROM loginSession WHERE userType = '" + 'Admin' + "'")
        cursor.execute(query)

        databaseCon.commit()

        query = ("INSERT INTO loginSession VALUES ('" + userID +"', '" + 'Admin' + "')")
        cursor.execute(query)

        databaseCon.commit()

        return render(request, "adminIndex.html")

    else:

        x = userID[0]

        if x == "D" or x == "d":

            query = ("DELETE FROM loginSession WHERE userType = '" + 'D' + "'")
            cursor.execute(query)

            databaseCon.commit()

            query = ("INSERT INTO loginSession VALUES ('" + userID + "', '" + 'D' + "')")
            cursor.execute(query)

            databaseCon.commit()

            return render(request, "driverIndex.html")

        elif x == "U" or x == "u":

            query = ("DELETE FROM loginSession WHERE userType = '" + 'U' + "'")
            cursor.execute(query)

            databaseCon.commit()

            query = ("INSERT INTO loginSession VALUES ('" + userID + "', '" + 'U' + "')")
            cursor.execute(query)

            databaseCon.commit()

            return render(request, "userIndex.html")

        return HttpResponse("User Not Found!")

def adminProcess(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    try:

        query_bookings = "SELECT COUNT(requestID) FROM endOfRide"
        cursor.execute(query_bookings)
        total_bookings = cursor.fetchone()[0]

        query_money = "SELECT SUM(totalrideRate) FROM endOfRide"
        cursor.execute(query_money)
        total_money = cursor.fetchone()[0] or 0

    finally:
        # Close database connection
        databaseCon.close()

    # Render the HTML template with data and pie chart image
    return render(request, "adminProcess.html", {
        'total_bookings': total_bookings,
        'total_money': total_money,
    })

def driverProcess(request):
    return render(request, "driverProcess.html")

def userProcess(request):
    return render(request, "userProcess.html")

def changePass(request):
    return render(request, "changePass.html")

def changePass1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    s1 = request.POST["t1"]
    s2 = request.POST["t2"]

    query = "SELECT * FROM loginCredentials WHERE UserID = 'Admin' and password = '" + s1 + "'"
    cursor.execute(query)

    if cursor.rowcount == 0:

        msg = "Incorrect Existing Password"
    else:

        query = "UPDATE loginCredentials SET password = '" + s2 + "' where UserID = 'Admin' "
        cursor.execute(query)

        databaseCon.commit()

        msg = "Password Updated Successfully"

    return render(request, "changePass.html", {
        'msg': msg
        })


def tuktukRegistration(request):
    return render(request, "tuktukRegistration.html")

def tuktukRegistration1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    VehicleNumber = request.POST["VehicleNumber"]
    vehicleType = request.POST["vehicleType"]
    fuelType = request.POST["fuelType"]
    manufacturedCompany = request.POST["manufacturedCompany"]
    vehicleCc = request.POST["vehicleCc"]
    year = request.POST["year"]
    RCUpload = request.FILES["RCUpload"]
    vehiclePhoto = request.FILES["vehiclePhoto"]
    DateOfRegistration = request.POST["DateOfRegistration"]
    #print(request.FILES)

    fs = FileSystemStorage()
    RCUploadName = fs.save("static/data/tuktukProof/dataProof/" + RCUpload.name, RCUpload)
    RCUploadName = RCUploadName[34:]
    vehiclePhotoName = fs.save("static/data/tuktukProof/dataProof/" + vehiclePhoto.name, vehiclePhoto)
    vehiclePhotoName = vehiclePhotoName[34:]

    query = ("SELECT * FROM tuktukData WHERE VehicleRegNo = '" + VehicleNumber + "'")
    cursor.execute(query)

    if cursor.rowcount > 0:

        msg = "Tuktuk Registration Already Exists"

    else:

        query = "INSERT INTO tuktukData VALUES ('" + VehicleNumber + "', '" + vehicleType + "', '"+ fuelType + "', '" + manufacturedCompany + "', '" + vehicleCc + "', '" + year + "', '" + RCUploadName + "', '" + vehiclePhotoName + "', '" + DateOfRegistration + "')"

        cursor.execute(query)
        databaseCon.commit()

        msg = "Tuktuk Registration Successful"

    return render(request, "tuktukRegistration.html", {
        'msg': msg
        })

def tuktukDriverRegistration(request):
    return render(request, "driverRegistration.html")

def tuktukDriverRegistration1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    driverName = request.POST["driverName"]
    houseName = request.POST["houseName"]
    placeName = request.POST["placeName"]
    pincode = request.POST["pincode"]
    email = request.POST["email"]
    phoneNumber = request.POST["phoneNumber"]
    driverGender = request.POST["driverGender"]
    driverGender = request.POST["driverGender"]
    dob = request.POST["dob"]
    aadhar = request.POST["aadhar"]
    license = request.POST["license"]
    driverPhoto = request.FILES["driverPhoto"]
    DateOfRegistration = request.POST["DateOfRegistration"]

    fs = FileSystemStorage()
    driverPhotoProof = fs.save("static/data/tuktukProof/dataProof/" + driverPhoto.name, driverPhoto)
    driverPhotoProof = driverPhotoProof[34:]

    driverID = "D1000"

    query = "SELECT * FROM tuktukDriverData ORDER BY driverID DESC"

    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]
        break
    x = driverID[1:]
    y = int(x)
    y = y + 1
    driverID = "D" + str(y)

    query = ("SELECT * FROM tuktukDriverData WHERE driverId = '" + driverID + "'")
    cursor.execute(query)

    msg =""

    query = "INSERT INTO tuktukDriverData VALUES ('" + driverID + "', '" + driverName + "', '" + houseName + "', '" + placeName + "', '" + pincode + "', '" + phoneNumber + "', '" + driverGender + "', '" + dob + "', '" + aadhar + "', '" + license +"', '" + driverPhotoProof + "', '" + DateOfRegistration + "')"
    cursor.execute(query)

    databaseCon.commit()

    query = "INSERT INTO loginCredentials values ('" + driverID + "', '" + email + "' ,'" + driverID + "')"
    cursor.execute(query)

    databaseCon.commit()

    msg = "Driver Registration Successfully Finished\n Default Password is your DriverID is " + driverID

    return render(request, "driverRegistration.html", {
        'msg': msg
        })

def tuktukAllot(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = ("SELECT VehicleRegNo FROM tuktukData")
    cursor.execute(query)

    records = cursor.fetchall()

    vehicleList = []

    for row in records:
        vehicleList.append(row[0])

    return render(request, "tuktukAllot.html", {
        'vehicleList': vehicleList
        })

def tuktukAllot1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    VehicleNumber = request.POST["VehicleNumber"]

    query = ("SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData WHERE VehicleRegNo = '" + VehicleNumber + "'")
    cursor.execute(query)

    records = cursor.fetchall()

    query = ("SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData")
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    return render(request, "allotDetails.html", {
        'VehicleNumber': VehicleNumber,
        'records': records,
        'driverRecords': driverRecords
        })


def tuktukAllot2(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    VehicleNumber = request.POST["VehicleNumber"]
    driverID = request.POST["driverID"]

    query = ("SELECT * FROM tuktukData WHERE VehicleRegNo = '" + VehicleNumber + "'")
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        vehicleType = row[1]
        vehicleFuelType = row[2]
        manufacturedCompany = row[3]
        Vcc = row[4]
        year = row[5]
        RC = row[6]
        vPhoto = row[7]
        regDate = row[8]

    query = ("SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData WHERE driverID = '" + driverID + "'")
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverName = row[1]
        phoneNumber = row[2]
        license = row[3]
        driverPhoto = row[4]

    return render(request, "allotingPage.html",{
        'VehicleNumber': VehicleNumber,
        'vehicleType': vehicleType,
        'vehicleFuelType': vehicleFuelType,
        'manufacturedCompany': manufacturedCompany,
        'Vcc': Vcc,
        'year': year,
        ' RC': RC,
        'vPhoto': vPhoto,
        'regDate': regDate,
        'driverID': driverID,
        'driverName': driverName,
        'phoneNumber': phoneNumber,
        'license': license,
        'driverPhoto': driverPhoto
        })

def tuktukAllot3(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    VehicleNumber = request.POST["VehicleNumber"]
    driverID = request.POST["driverID"]
    status = request.POST["status"]
    allotDate = currentDate()

    query = ("SELECT * FROM tuktukData WHERE VehicleRegNo = '" + VehicleNumber + "'")
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        vehicleType = row[1]
        vehicleFuelType = row[2]
        manufacturedCompany = row[3]
        Vcc = row[4]
        year = row[5]
        RC = row[6]
        vPhoto = row[7]
        regDate = row[8]

    query = ("SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData WHERE driverID = '" + driverID + "'")
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverName = row[1]
        phoneNumber = row[2]
        license = row[3]
        driverPhoto = row[4]

    query = ("UPDATE tuktukDriverAllot SET status = 'NO' WHERE VehicleRegNo = '" + VehicleNumber + "'")
    cursor.execute(query)

    databaseCon.commit()

    query = ("UPDATE tuktukDriverAllot SET status = 'NO' WHERE driverID = '" + driverID + "'")
    cursor.execute(query)

    databaseCon.commit()

    query = ("SELECT * FROM tuktukDriverAllot WHERE VehicleRegNo = '" + VehicleNumber + "' AND driverID = '" + driverID + "'")
    cursor.execute(query)

    existing_record = cursor.fetchone()

    if existing_record:
        msg = "Allotment for " + driverID + " with " + VehicleNumber + " is set to 'NO'."

    else:
        AllotID = "AID1000"

        query = "SELECT * FROM tuktukDriverAllot ORDER BY allotID DESC"
        cursor.execute(query)

        records = cursor.fetchall()

        for row in records:
            AllotID = row[0]
            break
        x = AllotID[3:]
        y = int(x)
        y = y + 1
        AllotID = "AID" + str(y)

        status = "YES"

        query = ("INSERT INTO tuktukDriverAllot VALUES ('" + AllotID + "', '" + VehicleNumber + "', '" + driverID + "', '" + allotDate + "', '" + status + "')")
        cursor.execute(query)

        databaseCon.commit()

        msg = driverID + " Alloted To " + VehicleNumber + " Tuktuk"

    return render(request, "allotingPage.html", {
        'VehicleNumber': VehicleNumber,
        'vehicleType': vehicleType,
        'vehicleFuelType': vehicleFuelType,
        'manufacturedCompany': manufacturedCompany,
        'Vcc': Vcc,
        'year': year,
        ' RC': RC,
        'vPhoto': vPhoto,
        'regDate': regDate,
        'driverID': driverID,
        'driverName': driverName,
        'phoneNumber': phoneNumber,
        'license': license,
        'driverPhoto': driverPhoto,
        'VehicleNumber': VehicleNumber,
        'driverID': driverID,
        'allotDate': allotDate,
        'status': status,
        'msg': msg
        })

def tuktukUserLogin(request):
    return render(request, "tuktukUserLogin.html")

def tuktukUserLoginRequests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    userName = request.POST["userName"]
    email = request.POST["email"]
    passBox1 = request.POST["passBox1"]
    DateOfRegistration = currentDate()

    userID = "U1000"

    query = "SELECT * FROM tuktukUserData ORDER BY userID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        userID = row[0]
        break
    x = userID[1:]
    y = int(x)
    y = y + 1
    userID = "U" + str(y)

    query = "INSERT INTO tuktukUserData VALUES('" + userID + "', '" + userName + "', '" + DateOfRegistration + "') "
    cursor.execute(query)

    databaseCon.commit()

    query = "INSERT INTO loginCredentials VALUES('" + userID + "', '" + email + "', '" + passBox1 + "')"
    cursor.execute(query)

    databaseCon.commit()

    msg = " User Login Successful \n your userID is " + userID

    return render(request, "tuktukUserLogin.html", {
        'msg': msg
        })

def userChangePass(request):
    return render(request, "userChangePass.html")

def userChangePass1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    oldPassword = request.POST["t1"]
    newPassword = request.POST["t2"]

    query = ("SELECT * FROM loginSession WHERE userType = 'U' ")
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        userID = row[0]

    query = ("SELECT * FROM loginCredentials WHERE UserID = '" + userID + "' AND password = '" + oldPassword + "'")
    cursor.execute(query)

    if cursor.rowcount == 0:
        msg = "Invalid Existing Password"

    else:
        query = ("UPDATE loginCredentials SET password = '" + newPassword +"' WHERE UserID = '" + userID + "'")
        cursor.execute(query)

        databaseCon.commit()

        msg = "Password Updated Successfully"

    return render(request, "userChangePass.html", {
        'msg': msg
        })

def driverChangePass(request):
    return render(request, "driverChangePass.html")

def driverChangePass1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    oldPassword = request.POST["t1"]
    newPassword = request.POST["t2"]

    query = ("SELECT * FROM loginSession WHERE userType = 'D' ")
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = ("SELECT * FROM loginCredentials WHERE UserID = '" + driverID + "' AND password = '" + oldPassword + "'")
    cursor.execute(query)

    if cursor.rowcount == 0:
        msg = "Invalid Existing Password"

    else:
        query = ("UPDATE loginCredentials SET password = '" + newPassword +"' WHERE UserID = '" + driverID + "'")
        cursor.execute(query)

        databaseCon.commit()

        msg = "Password Updated Successfully"

    return render(request, "driverChangePass.html", {
        'msg': msg
        })

def tuktukDetails(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = ("SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData")
    cursor.execute(query)

    records = cursor.fetchall()

    query = ("SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData")
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    return render(request, "tuktukDetails.html", {
        'records': records,
        'driverRecords': driverRecords
        })

def feedback(request):
    return render(request, "feedback.html")

def userFeedback(request):
    return render(request, "userfeedback.html")

def feedback1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedArea = request.POST["feedArea"]
    name = request.POST["name"]
    email = request.POST["email"]

    feedbackDate = currentDate()

    feedbackID = 1000

    query = "SELECT * FROM feedback ORDER BY feedbackID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedbackID = row[0]
        break
    x = feedbackID
    x = x + 1
    feedbackID = x

    query = "SELECT * FROM loginSession WHERE userType = 'D'"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = ("INSERT INTO feedback (feedbackID, feedback, feedbackDate, driverID, name, email) VALUES ('" + str(feedbackID) + "', '" + feedArea + "', '" + feedbackDate + "', '" + driverID + "', '" + name + "', '" + email + "')")
    #print(query)
    cursor.execute(query)

    databaseCon.commit()

    return render(request, "feedback.html", {
        'feedbackID': feedbackID,
        'feedArea': feedArea,
        'feedbackDate': feedbackDate,
        'driverID': driverID,
        'name': name,
        'email': email})

def userFeedback1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedArea = request.POST["feedArea"]
    name = request.POST["name"]
    email = request.POST["email"]

    feedbackDate = currentDate()

    feedbackID = 1000

    query = "SELECT * FROM feedback ORDER BY feedbackID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedbackID = row[0]
        break
    x = feedbackID
    x = x + 1
    feedbackID = x

    query = "SELECT * FROM loginSession WHERE userType = 'U' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        userID = row[0]
    # print(records)

    query = ("INSERT INTO feedback (feedbackID, feedback, feedbackDate, userID, name, email) VALUES ('" + str(feedbackID) + "', '" + feedArea + "', '" + feedbackDate + "', '" + userID + "', '" + name + "', '" + email + "')")
    cursor.execute(query)

    databaseCon.commit()

    return render(request, "userFeedback.html", {
        'feedbackID': feedbackID,
        'feedArea': feedArea,
        'feedbackDate': feedbackDate,
        'userID': userID,
        'name': name,
        'email': email})

def feedReply(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = ("SELECT feedbackID FROM feedback WHERE driverID IS NOT NULL AND reply IS NULL")
    cursor.execute(query)

    records = cursor.fetchall()

    feedbacks = []
    for row in records:
        feedbacks.append(row[0])

    return render(request, "feedReply.html", {
        "feedbacks": feedbacks
        })

def userFeedbackReply(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = ("SELECT feedbackID FROM feedback WHERE userID IS NOT NULL AND reply IS NULL")
    cursor.execute(query)

    records = cursor.fetchall()

    userFeedbacks = []

    for row in records:
        userFeedbacks.append(row[0])

    return render(request, "userFeedbackReply.html", {
        "userFeedbacks": userFeedbacks
        })

def feedReplyRequests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]

    query = ("SELECT * FROM feedback WHERE  feedbackID = '" + feedbackID + "'")
    # print(query)
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedback = row[1]
        feedbackDate = row[2]
        driverID = row[4]

    query = ("SELECT * FROM tuktukDriverData WHERE driverID = '" + driverID + "'")
    #print(query)
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverID = row[0]
        driverName = row[1]
        phoneNumber = row[5]
        license = row[9]
        driverPhoto = row[10]

    return render(request, "feedbackDetails.html", {
        'feedbackID': feedbackID,
        'feedback': feedback,
        'feedbackDate': feedbackDate,
        'driverID': driverID,
        'driverName': driverName,
        'phoneNumber': phoneNumber,
        'license': license,
        'driverPhoto': driverPhoto})

def userFeedbackReplyRequests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]

    query = ("SELECT * FROM feedback WHERE feedbackID = '" + feedbackID + "'")
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedback = row[1]
        feedbackDate = row[2]
        userID = row[3]

    query = ("SELECT * FROM tuktukUserData WHERE userID = '" + userID + "'")
    cursor.execute(query)

    userRecords = cursor.fetchall()

    for row in userRecords:
        userID = row[0]
        userName = row[1]
        place = row[2]
        phoneNumber = row[3]

    return render(request, "userFeedbackDetails.html", {
        "feedbackID": feedbackID,
        "feedback": feedback,
        "feedbackDate": feedbackDate,
        "userID": userID,
        "userName": userName,
        "place": place,
        "phoneNumber": phoneNumber})

def feedbackDetailsPost(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]
    textarea = request.POST["textarea"]
    replyDate = currentDate()

    query = ("SELECT * FROM feedback WHERE  feedbackID = '" + feedbackID + "'")
    #print(query)
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedback = row[1]
        feedbackDate = row[2]
        driverID = row[4]

    query = ("SELECT * FROM tuktukDriverData WHERE driverID = '" + driverID + "'")
    #print(query)
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverID = row[0]
        driverName = row[1]
        phoneNumber = row[5]
        license = row[9]
        driverPhoto = row[10]

    query = ("UPDATE feedback SET reply = '" + textarea + "', replyDate = '" + replyDate + "' WHERE feedbackID = '" + feedbackID + "'")
    cursor.execute(query)

    databaseCon.commit()

    msg = "Replied.."

    return render(request, "feedbackDetails.html", {
        'feedbackID': feedbackID,
        'feedback': feedback,
        'feedbackDate': feedbackDate,
        'driverID': driverID,
        'driverName': driverName,
        'phoneNumber': phoneNumber,
        'license': license,
        'driverPhoto': driverPhoto,
        'msg': msg})

def userFeedbackDetailsPost(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]
    textarea = request.POST["textarea"]
    replyDate= currentDate()

    query = "SELECT * FROM feedback WHERE feedbackID = '" + feedbackID + "'"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedback = row[1]
        feedbackDate = row[2]
        userID = row[3]

    query = "SELECT * FROM tuktukUserData WHERE userID = '" + userID + "'"
    cursor.execute(query)

    userRecords = cursor.fetchall()

    for row in userRecords:
        userID = row[0]
        userName = row[1]
        place = row[3]
        phoneNumber = row[4]

    query = "UPDATE feedback SET reply = '" + textarea + "', replyDate = '" + replyDate + "' WHERE feedbackID = '" + feedbackID + "'"
    cursor.execute(query)

    databaseCon.commit()

    msg = "Replied.."

    return render(request, "userFeedbackDetails.html", {
        "feedbackID": feedbackID,
        "feedback": feedback,
        "userID": userID,
        "userName": userName,
        "place": place,
        "phoneNumber": phoneNumber,
        "msg": msg})

# List of auto locations

def bookingPage(request):
    return render(request, 'bookingPage.html')

auto_locations = [
    {'id': "KL01B4346", 'lat': 9.152091, 'lon': 76.738282},
    {'id': "KL05L6452", 'lat': 9.154538, 'lon': 76.732662},
    {'id': "KL23A6767", 'lat': 9.132163, 'lon': 76.768493},
    {'id': "KL65J9284", 'lat': 9.149356, 'lon': 76.755677}
]

ids = [auto['id'] for auto in auto_locations]
first_id = ids[0]

# print(first_id)

logger = logging.getLogger(__name__)

def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

    headers = {
        'User-Agent': 'mapping (adithyanprdev@gmail.com)'  # Replace with your application name and contact information
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('display_name')

# Function to connect to the MySQL database and fetch fare estimation parameters
def get_fare_parameters():
    try:
        databaseCon = connectdb()
        cursor = databaseCon.cursor()

        query = "SELECT minimumFare, farePerKm, waitingFare, minimumKM FROM fareEstimation ORDER BY fareNO DESC"
        cursor.execute(query)
        result = cursor.fetchone()  # Fetch one row as we only need the latest fare parameters

        if result:
            fare_params = {
                'minimumFare': float(result[0]),
                'farePerKm': float(result[1]),
                'waitingFare': float(result[2]),
                'minimumKM': float(result[3])
            }
            print("Fare Parameters: ", fare_params)  # Debug statement
            return fare_params
        else:
            raise Exception("Fare estimation parameters not found")
    finally:
        databaseCon.close()

def calculate_fare(distance, fare_params):
    if distance <= fare_params['minimumKM']:
        return fare_params['minimumFare']
    else:
        return fare_params['minimumFare'] + (distance - fare_params['minimumKM']) * fare_params['farePerKm']

@csrf_exempt
def calculate_distance_and_allot_auto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_lat = float(data.get('user_lat'))
            user_lon = float(data.get('user_lon'))
            dest_name = data.get('dest_name')
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error("Invalid JSON or missing data: %s", e)
            return JsonResponse({'error': 'Invalid JSON or missing data'}, status=400)

        api_key = '5b3ce3597851110001cf6248d0882d4d8035451eb97f11ef667f07b1'
        geocode_url = f'https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={dest_name}'

        try:
            geocode_response = requests.get(geocode_url)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()
        except requests.RequestException as e:
            logger.error("Error fetching geocode data: %s", e)
            return JsonResponse({'error': 'Error fetching geocode data', 'details': str(e)}, status=500)

        if 'features' not in geocode_data or not geocode_data['features']:
            logger.error("Destination not found for: %s", dest_name)
            return JsonResponse({'error': 'Destination not found'}, status=404)

        destination = geocode_data['features'][0]['geometry']['coordinates']
        dest_lon, dest_lat = destination

        # Calculate the distance between user and destination using OpenRouteService
        route_url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={user_lon},{user_lat}&end={dest_lon},{dest_lat}'
        try:
            route_response = requests.get(route_url)
            route_response.raise_for_status()
            route_data = route_response.json()
            distance_to_destination = route_data['features'][0]['properties']['segments'][0]['distance'] / 1000  # convert to km
        except requests.RequestException as e:
            logger.error("Error fetching route data: %s", e)
            return JsonResponse({'error': 'Error fetching route data', 'details': str(e)}, status=500)

        min_distance = float('inf')
        nearest_auto = None

        # Finding the nearest auto
        for auto in auto_locations:
            auto_lat = auto['lat']
            auto_lon = auto['lon']
            distance = haversine(user_lat, user_lon, auto_lat, auto_lon)

            if distance < min_distance:
                min_distance = distance
                nearest_auto = auto.copy()  # Make a copy to avoid modifying the original dict

        if nearest_auto:
            nearest_auto['location'] = reverse_geocode(nearest_auto['lat'], nearest_auto['lon'])

            # Fetch fare parameters
            try:
                fare_params = get_fare_parameters()
            except Exception as e:
                logger.error("Error fetching fare parameters: %s", e)
                return JsonResponse({'error': 'Error fetching fare parameters', 'details': str(e)}, status=500)

            # Calculate fare based on distance to destination
            fare = calculate_fare(distance_to_destination, fare_params)

            return JsonResponse({
                'distance': min_distance,
                'nearest_auto': nearest_auto,
                'destination_lat': dest_lat,
                'destination_lon': dest_lon,
                'fare_estimation': fare
            }, status=200)
        else:
            logger.error("No autos available")
            return JsonResponse({'error': 'No autos available'}, status=404)
    else:
        logger.error("Method not allowed")
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def haversine(lat1, lon1, lat2, lon2):
    import math
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance



def mapView(request):
    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT vehicleRegNo FROM tuktukRequest ORDER BY requestID DESC"
    cursor.execute(query)
    print(query)

    records = cursor.fetchall()

    for row in records:
        vehicleRegNo = row[0]

    driver_query = "SELECT dl.VehicleRegNo, dl.tuktukLatitude, dl.tuktukLongitude FROM driverLocation dl INNER JOIN tuktukRequest tr ON dl.VehicleRegNo = tr.vehicleRegNo ORDER BY tr.requestID"
    cursor.execute(driver_query)
    driver_records = cursor.fetchall()

    # Fetch user data
    user_query = "SELECT userID, userLat, userLon, destination FROM tuktukRequest ORDER BY requestID"
    cursor.execute(user_query)
    user_records = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    databaseCon.close()

    # Convert Decimal to float and prepare data
    driver_data = []
    for record in driver_records:
        vehicleRegNo = record[0]
        tuktukLatitude = float(record[1])
        tuktukLongitude = float(record[2])
        driver_data.append({'vehicleRegNo': vehicleRegNo, 'latitude': tuktukLatitude, 'longitude': tuktukLongitude})

    user_data = []
    for record in user_records:
        userID = record[0]
        userLat = float(record[1])
        userLon = float(record[2])
        destination = record[3]
        user_data.append({'userID': userID, 'latitude': userLat, 'longitude': userLon, 'destination': destination})

    return render(request, "mapView.html", {'driver_data': driver_data, 'user_data': user_data})

def driverRideDetails(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    requestID = request.POST["requestID"]

    totalDistance = request.POST["totalDistance"]
    waitingCharge = request.POST["waitingCharge"]

    query = "SELECT requestID FROM tuktukResponse ORDER BY requestID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]

    query = "SELECT * FROM fareEstimation ORDER BY fareNO desc"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        minimumFare = row[1]
        farePerKm = row[2]
        waitingFare = row[3]
        minimumKM = row[5]

    if int(totalDistance) <= minimumKM:
        fare = minimumFare
    else:
        fareMinKM = int(totalDistance) - minimumKM
        fareMinKMperKm = fareMinKM * farePerKm
        fare = minimumFare + fareMinKMperKm

    wcmin = waitingFare / 60

    if int(waitingCharge) >= 10:
       wcCharge =  wcmin * int(waitingCharge)
    else:
        wcCharge = 0

    totalRideRate = fare + wcCharge

    return render(request, "driverRideDetails.html", {
        'requestID': requestID,
        'waitingCharge': waitingCharge,
        'totalDistance': totalDistance
        })

def requetTuktukAndTuktukDriver(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    userLat = request.POST["userLat"]
    userLon = request.POST["userLon"]

    nearestAutoID = request.POST["nearestAutoID"]

    destCoordinates = request.POST["destCoordinates"]

    requestDate = currentDate()
    requestTime = time.strftime('%H:%M:%S')

    distance = request.POST["distance"]

    requestID = "R1000"

    query = "SELECT * FROM tuktukRequest ORDER BY requestID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]
        break
    x = requestID[1:]
    y = int(x)
    y = y + 1
    requestID = "R" + str(y)

    query = "SELECT * FROM tuktukDriverAllot WHERE VehicleRegNo = '" + nearestAutoID + "' AND status = 'YES'"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[2]

    query = "SELECT * FROM loginSession WHERE userType = 'U' "
    cursor.execute(query)
    # print(query)

    records = cursor.fetchall()

    for row in records:
        userID = row[0]

    query = "INSERT INTO tuktukRequest VALUES ('" + requestID + "', '" + userID + "', '" + destCoordinates + "' ,'" + requestDate + "', '" + requestTime + "', '" + nearestAutoID + "', '" + userLat + "', '" + userLon + "', '" + driverID + "', '" + distance + "')"
    cursor.execute(query)

    databaseCon.commit()

    return redirect('rideDetails')

def loading(request):
    return render(request, 'loading.html')

def checkDriverResponse(request):
    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    # Fetching requestID from session or POST data
    requestID = request.session.get('requestID')

    # Implement logic to check if the driver has responded
    query = f"SELECT response FROM tuktukResponse WHERE requestID = '{requestID}' ORDER BY responseDate DESC, responseTime DESC LIMIT 1"
    cursor.execute(query)
    response = cursor.fetchone()

    if response and response[0] == 'YES':
        # Driver has responded
        return JsonResponse({'response': True})
    else:
        # Driver has not responded yet
        return JsonResponse({'response': False})


def responseForTuktuk(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT * FROM loginSession WHERE userType = 'D' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = 'SELECT * FROM tuktukRequest WHERE driverID = "' + driverID + '" AND requestID NOT IN (SELECT requestID FROM tuktukResponse)'
    cursor.execute(query)

    records = cursor.fetchall()

    if cursor.rowcount == 0:
        msg = "No Requests"
        return render(request, "noResponseForTuktuk.html", {
            'msg': msg
            })

    else :

        for row in records:
            requestID = row[0]
            driverID = row[1]
            userLat = row[6]
            userLon = row[7]
            destination = row[2]

        query = "SELECT * FROM loginSession WHERE userType = 'U' "
        cursor.execute(query)

        records = cursor.fetchall()

        for row in records:
            userID = row[0]

        query = "SELECT userName FROM tuktukUserData WHERE userID = '" + userID + "'"
        cursor.execute(query)
        # print(query)

        records = cursor.fetchall()

        for row in records:
            userName = row[0]


        return render(request, "responseForTuktuk.html", {
            'requestID': requestID,
            'userName': userName,
            'driverID': driverID,
            'userLat': userLat,
            'userLon': userLon,
            'destination': destination})

def responseForTuktukRequests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    requestID = request.POST["requestID"]
    response = request.POST["response"]

    responseTime = time.strftime('%H:%M:%S')
    responseDate = currentDate()

    query = "SELECT * FROM loginSession WHERE userType = 'D' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = 'SELECT * FROM tuktukRequest WHERE driverID = "' + driverID + '" AND requestID NOT IN (SELECT requestID FROM tuktukResponse)'
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]
        driverID = row[1]
        userLat = row[6]
        userLon = row[7]
        destination = row[2]

    query = "SELECT * FROM loginSession WHERE userType = 'U' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        userID = row[0]

    query = "SELECT userName FROM tuktukUserData WHERE userID = '" + userID + "'"
    cursor.execute(query)
    # print(query)

    records = cursor.fetchall()

    for row in records:
        userName = row[0]

    query = "INSERT INTO tuktukResponse VALUES ('" + requestID + "', '" + responseTime + "', '" + responseDate + "', '" + response + "')"
    cursor.execute(query)

    databaseCon.commit()

    message = "Response Submitted"


    return render(request, "responseForTuktuk.html", {
        'requestID': requestID,
        'userName': userName,
        'driverID': driverID,
        'userLat': userLat,
        'userLon': userLon,
        'destination': destination,
        "message": message})

def fareEstimation(request):
    return render(request, "fareEstimation.html")

def fareEstimationRequets(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    fareNO = 1

    query = "SELECT * FROM fareEstimation ORDER BY fareNO DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        fareNO = row[0]
        break
    x = fareNO
    x = x + 1
    fareNO = x

    minFare = request.POST["minFare"]
    farePerKm = request.POST["farePerKm"]
    WaitingCharges = request.POST["WaitingCharges"]
    MinimumKM = request.POST["MinimumKM"]

    currentDateOfChange = currentDate()

    query = "INSERT INTO fareEstimation VALUES ('" + str(fareNO) + "', '" + minFare + "', '" + farePerKm + "', '" + WaitingCharges + "', '" + currentDateOfChange + "', '" + MinimumKM + "')"
    cursor.execute(query)

    databaseCon.commit()

    message = "New fare details submitted..."

    return render(request, "fareEstimation.html", {
        'message': message
        })

def rideDetails(request):
    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    if request.method == 'POST':
        # Fetch latest details from database
        responseTime = time.strftime('%H:%M:%S')
        responseDate = currentDate()

        # Get driverID from loginSession where userType is 'D'
        query = "SELECT * FROM loginSession WHERE userType = 'D'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            driverID = row[0]

        # Get driver details
        query = "SELECT driverName, driverPhoto FROM tuktukDriverData WHERE driverID = '" + driverID + "'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            driverName = row[0]
            driverPhoto = row[1]

        # Get tuktuk request details
        query = 'SELECT * FROM tuktukRequest WHERE driverID = "' + driverID + '"'
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            requestID = row[0]
            userLat = row[6]
            userLon = row[7]
            destination = row[2]

        # Get userID from loginSession where userType is 'U'
        query = "SELECT * FROM loginSession WHERE userType = 'U'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            userID = row[0]

        # Get user name
        query = "SELECT userName FROM tuktukUserData WHERE userID = '" + userID + "'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            userName = row[0]

        # Get response details
        query = "SELECT response, responseTime, responseDate FROM tuktukResponse WHERE requestID = '" + requestID + "'"
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            for row in records:
                response = row[0]
                responseTime = row[1]
                responseDate = row[2]
        else:
            response = "No response yet"
            responseTime = ""
            responseDate = ""

        # Get VehicleRegNo
        query = "SELECT VehicleRegNo FROM tuktukDriverAllot WHERE driverID = '" + driverID + "' AND status = 'YES'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            VehicleRegNo = row[0]

        message = "You can Identify your Tuktuk & Driver using this Details"

        return render(request, "rideDetails.html", {
            'requestID': requestID,
            'userName': userName,
            'userLat': userLat,
            'userLon': userLon,
            'destination': destination,
            'response': response,
            'responseTime': responseTime,
            'responseDate': responseDate,
            'driverID': driverID,
            'driverPhoto': driverPhoto,
            'driverName': driverName,
            'VehicleRegNo': VehicleRegNo,
            'message': message
        })

    else:  # GET request
        # Initially load the details
        responseTime = time.strftime('%H:%M:%S')
        responseDate = currentDate()

        # Get driverID from loginSession where userType is 'D'
        query = "SELECT * FROM loginSession WHERE userType = 'D'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            driverID = row[0]

        # Get driver details
        query = "SELECT driverName, driverPhoto FROM tuktukDriverData WHERE driverID = '" + driverID + "'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            driverName = row[0]
            driverPhoto = row[1]

        # Get tuktuk request details
        query = 'SELECT * FROM tuktukRequest WHERE driverID = "' + driverID + '"'
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            requestID = row[0]
            userLat = row[6]
            userLon = row[7]
            destination = row[2]

        # Get userID from loginSession where userType is 'U'
        query = "SELECT * FROM loginSession WHERE userType = 'U'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            userID = row[0]

        # Get user name
        query = "SELECT userName FROM tuktukUserData WHERE userID = '" + userID + "'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            userName = row[0]

        # Get response details
        query = "SELECT response, responseTime, responseDate FROM tuktukResponse WHERE requestID = '" + requestID + "'"
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            for row in records:
                response = row[0]
                responseTime = row[1]
                responseDate = row[2]
        else:
            response = "No response yet"
            responseTime = ""
            responseDate = ""

        # Get VehicleRegNo
        query = "SELECT VehicleRegNo FROM tuktukDriverAllot WHERE driverID = '" + driverID + "' AND status = 'YES'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            VehicleRegNo = row[0]

        message = "You can Identify your Tuktuk & Driver using this Details"

        return render(request, "rideDetails.html", {
            'requestID': requestID,
            'userName': userName,
            'userLat': userLat,
            'userLon': userLon,
            'destination': destination,
            'response': response,
            'responseTime': responseTime,
            'responseDate': responseDate,
            'driverID': driverID,
            'driverPhoto': driverPhoto,
            'driverName': driverName,
            'VehicleRegNo': VehicleRegNo,
            'message': message
        })

def checkDriverResponse(request):
    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    # Fetching requestID from session or POST data
    requestID = request.session.get('requestID')

    # Implement logic to check if the driver has responded
    if not requestID:
        return JsonResponse({'response': False})

    query = f"SELECT response FROM tuktukResponse WHERE requestID = '{requestID}' ORDER BY responseDate DESC, responseTime DESC LIMIT 1"
    cursor.execute(query)
    response = cursor.fetchone()

    if response and response[0] == 'YES':
        # Driver has responded
        return JsonResponse({'response': True})
    else:
        # Driver has not responded yet
        return JsonResponse({'response': False})

# def mapView(request):
#     return render(request, "mapView.html")

def onGoingRide(request):
    return render(request, "onGoingRide.html")

def onGoingRideRequests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    minFare = request.POST["minFare"]
    WaitingCharges = request.POST["WaitingCharges"]
    comment = request.POST["comment"]

    onGoingRideDate = currentDate()
    onGoingRideTime = time.strftime('%H:%M:%S')

    query = "SELECT * FROM loginSession WHERE userType = 'D' "
    cursor.execute(query)
    # print(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = "SELECT requestID FROM tuktukRequest WHERE driverID = '" + driverID + "'"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]

    query = "INSERT INTO onGoingRide VALUES ('" + requestID + "', '" + minFare + "', '" + WaitingCharges + "', '" + onGoingRideDate + "', '" + onGoingRideTime + "', '" + comment + "') "
    cursor.execute(query)

    databaseCon.commit()

    message = "Ride Completed! Thank You!!"

    return render(request, "onGoingRide.html", {
        'message': message
        })

def userList(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = ("SELECT userID, userName, dateOfRegistration FROM tuktukUserData")
    cursor.execute(query)

    records = cursor.fetchall()

    return render(request, "userList.html", {
        'records': records
        })

def tuktukForDriver(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT VehicleRegNo FROM tuktukDriverAllot"
    cursor.execute(query)

    records = cursor.fetchall()

    query = ("SELECT VehicleRegNo FROM tuktukDriverAllot WHERE status = 'YES'")
    cursor.execute(query)
    # print(query)

    records = cursor.fetchall()

    vehicleList = []

    for row in records:
        vehicleList.append(row[0])

    return render(request, "tuktukForDriver.html", {'vehicleList': vehicleList})

def tuktukForDriverDetails(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    vehicleNumber = request.POST["vehicleNumber"]
    # print(vehicleNumber)

    query = "SELECT * from tuktukDriverAllot where VehicleRegNo = '" + vehicleNumber + "' AND status = 'YES'"
    cursor.execute(query)
    # print(query)

    records = cursor.fetchall()

    for row in records:
        VehicleRegNo = row[1]
        driverID = row[2]

    query = "SELECT driverID FROM tuktukDriverAllot WHERE driverID = '" + driverID + "'"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = "SELECT * FROM tuktukDriverData WHERE driverID = '" + driverID + "'"
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverID = row[0]
        driverName = row[1]
        phoneNumber = row[5]
        license = row[9]
        driverPhoto = row[10]

    query = "SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData WHERE VehicleRegNo = '" + vehicleNumber + "'"
    cursor.execute(query)

    vehicleRecords = cursor.fetchall()

    for row in vehicleRecords:
        VehicleRegNo = row[0]
        vehicleType = row[1]
        vehicleFuelType = row[2]
        manufacturedCompany = row[3]
        Vcc = row[4]
        manufactureYear = row[5]
        RC = row[6]
        vPhoto = row[7]
        regDate = row[8]

    return render(request, "tuktukForDriverDetails.html", {
        'vehicleNumber': vehicleNumber,
        'vehicleType': vehicleType,
        'vehicleFuelType': vehicleFuelType,
        'manufacturedCompany': manufacturedCompany,
        'Vcc': Vcc,
        'manufactureYear': manufactureYear,
        'RC': RC,
        'vPhoto': vPhoto,
        'regDate': regDate,
        'driverID': driverID,
        'driverName': driverName,
        'phoneNumber': phoneNumber,
        'license': license,
        'driverPhoto': driverPhoto})

def driverForTuktuk(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = ("SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData")
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    return render(request, "driverForTuktuk.html", {
        'driverRecords': driverRecords
        })

def driverForTuktukDetails(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    driverID = request.POST["driverID"]

    query = "SELECT status, VehicleRegNo FROM tuktukDriverAllot WHERE driverID = '" + driverID + "' AND status = 'YES' AND VehicleRegNo IN (SELECT VehicleRegNo FROM tuktukDriverAllot WHERE status = 'YES')"
    cursor.execute(query)

    records = cursor.fetchall()

    if not records:
        message = "This driver is not alloted any TukTuk"
        return render(request, "driverForTuktukDetails.html", {'message': message})

    status, VehicleRegNo = records[0]

    query = "SELECT * FROM tuktukDriverData WHERE driverID = '" + driverID + "'"
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverID = row[0]
        driverName = row[1]
        phoneNumber = row[5]
        license = row[9]
        driverPhoto = row[10]

    query = "SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData WHERE VehicleRegNo = '" + VehicleRegNo + "'"
    cursor.execute(query)

    vehicleRecords = cursor.fetchall()

    for row in vehicleRecords:
        VehicleRegNo = row[0]
        vehicleType = row[1]
        vehicleFuelType = row[2]
        manufacturedCompany = row[3]
        Vcc = row[4]
        manufactureYear = row[5]
        RC = row[6]
        vPhoto = row[7]
        regDate = row[8]

    return render(request, "driverForTuktukDetails.html", {
        'status': status,
        'VehicleRegNo': VehicleRegNo,
        'vehicleType': vehicleType,
        'vehicleFuelType': vehicleFuelType,
        'manufacturedCompany': manufacturedCompany,
        'Vcc': Vcc,
        'manufactureYear': manufactureYear,
        'RC': RC,
        'vPhoto': vPhoto,
        'regDate': regDate,
        'driverID': driverID,
        'driverName': driverName,
        'phoneNumber': phoneNumber,
        'license': license,
        'driverPhoto': driverPhoto
    })

def starFeedback(request):
    return render(request, "starFeedback.html")

def receipt(request):
    return render(request, "receipt.html")

def receiptRequests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    totalDistance = request.POST["totalDistance"]
    waitingCharge = request.POST["waitingCharge"]

    emotionFeedback = request.POST["emotionFeedback"]

    endOfRideDate = currentDate()
    endOfRideTime = time.strftime('%H:%M:%S')


    query = "SELECT * FROM fareEstimation ORDER BY fareNO desc"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        minimumFare = row[1]
        farePerKm = row[2]
        waitingFare = row[3]
        minimumKM = row[5]

    if int(totalDistance) <= minimumKM:
        fare = minimumFare
    else:
        fareMinKM = int(totalDistance) - minimumKM
        fareMinKMperKm = fareMinKM * farePerKm
        fare = minimumFare + fareMinKMperKm

    wcmin = waitingFare / 60

    if int(waitingCharge) >= 10:
       wcCharge =  wcmin * int(waitingCharge)
    else:
        wcCharge = 0

    totalRideRate = fare + wcCharge

    query = "SELECT requestID FROM tuktukResponse ORDER BY requestID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]

    query = "INSERT INTO endOfRide (requestID, totalRideRate, waitingCharges, endOfRideDate, endOfRideTime, totalDistance, emotionFeedback) VALUES('" + requestID + "', '" + str(totalRideRate) + "', '" + waitingCharge + "', '" + endOfRideDate + "', '" + endOfRideTime + "', '" + totalDistance + "', '" + emotionFeedback + "')"
    cursor.execute(query)

    databaseCon.commit()

    message = "Thank You! For The ride"
    return render(request, "receipt.html", {
        'requestID': requestID,
        'totalRideRate': totalRideRate,
        'waitingCharge': waitingCharge,
        'endOfRideDate': endOfRideDate,
        'endOfRideTime': endOfRideTime,
        'totalDistance': totalDistance,
        'emotionFeedback': emotionFeedback,
        'message': message
        })
