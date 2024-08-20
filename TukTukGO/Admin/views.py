from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from TukTukGO import connectdb, currentDate

# Create your views here.


def sign_up_page(request):
    return render(request, "signUp.html")


def admin_process(request):

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
    return render(
        request,
        "adminProcess.html",
        {
            "total_bookings": total_bookings,
            "total_money": total_money,
        },
    )


def change_pass(request):
    return render(request, "changePass.html")


def change_pass_1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    s1 = request.POST["t1"]
    s2 = request.POST["t2"]

    query = "SELECT * FROM loginCredentials WHERE UserID = %s AND password = %s"
    cursor.execute(query, ("Admin", s1))

    if cursor.rowcount == 0:

        msg = "Incorrect Existing Password"
    else:

        query = "UPDATE loginCredentials SET password = %s WHERE UserID = %s"
        cursor.execute(query, (s2, "Admin"))

        databaseCon.commit()

        msg = "Password Updated Successfully"

    return render(request, "changePass.html", {"msg": msg})


def tuktuk_registration(request):
    return render(request, "tuktukRegistration.html")


def tuktuk_registration_1(request):

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
    # print(request.FILES)

    fs = FileSystemStorage()
    RCUploadName = fs.save(
        "static/data/tuktukProof/dataProof/" + RCUpload.name, RCUpload
    )
    RCUploadName = RCUploadName[34:]
    vehiclePhotoName = fs.save(
        "static/data/tuktukProof/dataProof/" + vehiclePhoto.name, vehiclePhoto
    )
    vehiclePhotoName = vehiclePhotoName[34:]

    query = "SELECT * FROM tuktukData WHERE VehicleRegNo = %s"
    cursor.execute(query, (VehicleNumber,))

    if cursor.rowcount > 0:

        msg = "Tuktuk Registration Already Exists"

    else:

        query = "INSERT INTO tuktukData (VehicleNumber, vehicleType, fuelType, manufacturedCompany, vehicleCc, year, RCUploadName, vehiclePhotoName, DateOfRegistration VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(
            query,
            (
                VehicleNumber,
                vehicleType,
                fuelType,
                manufacturedCompany,
                vehicleCc,
                year,
                RCUploadName,
                vehiclePhotoName,
                DateOfRegistration,
            ),
        )
        databaseCon.commit()

        msg = "Tuktuk Registration Successful"

    return render(request, "tuktukRegistration.html", {"msg": msg})


def tuktuk_driver_registration(request):
    return render(request, "driverRegistration.html")


def tuktuk_driver_registration_1(request):

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
    driverPhotoProof = fs.save(
        "static/data/tuktukProof/dataProof/" + driverPhoto.name, driverPhoto
    )
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

    query = "SELECT * FROM tuktukDriverData WHERE driverId = '" + driverID + "'"
    cursor.execute(query)

    msg = ""

    query = (
        "INSERT INTO tuktukDriverData VALUES ('"
        + driverID
        + "', '"
        + driverName
        + "', '"
        + houseName
        + "', '"
        + placeName
        + "', '"
        + pincode
        + "', '"
        + phoneNumber
        + "', '"
        + driverGender
        + "', '"
        + dob
        + "', '"
        + aadhar
        + "', '"
        + license
        + "', '"
        + driverPhotoProof
        + "', '"
        + DateOfRegistration
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    query = (
        "INSERT INTO loginCredentials values ('"
        + driverID
        + "', '"
        + email
        + "' ,'"
        + driverID
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    msg = (
        "Driver Registration Successfully Finished\n Default Password is your DriverID is "
        + driverID
    )

    return render(request, "driverRegistration.html", {"msg": msg})


def tuktuk_allot(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT VehicleRegNo FROM tuktukData"
    cursor.execute(query)

    records = cursor.fetchall()

    vehicleList = []

    for row in records:
        vehicleList.append(row[0])

    return render(request, "tuktukAllot.html", {"vehicleList": vehicleList})


def tuktuk_allot_1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    VehicleNumber = request.POST["VehicleNumber"]

    query = (
        "SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData WHERE VehicleRegNo = '"
        + VehicleNumber
        + "'"
    )
    cursor.execute(query)

    records = cursor.fetchall()

    query = "SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData"
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    return render(
        request,
        "allotDetails.html",
        {
            "VehicleNumber": VehicleNumber,
            "records": records,
            "driverRecords": driverRecords,
        },
    )


def tuktuk_allot_2(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    VehicleNumber = request.POST["VehicleNumber"]
    driverID = request.POST["driverID"]

    query = "SELECT * FROM tuktukData WHERE VehicleRegNo = '" + VehicleNumber + "'"
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

    query = (
        "SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData WHERE driverID = '"
        + driverID
        + "'"
    )
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverName = row[1]
        phoneNumber = row[2]
        license = row[3]
        driverPhoto = row[4]

    return render(
        request,
        "allotingPage.html",
        {
            "VehicleNumber": VehicleNumber,
            "vehicleType": vehicleType,
            "vehicleFuelType": vehicleFuelType,
            "manufacturedCompany": manufacturedCompany,
            "Vcc": Vcc,
            "year": year,
            " RC": RC,
            "vPhoto": vPhoto,
            "regDate": regDate,
            "driverID": driverID,
            "driverName": driverName,
            "phoneNumber": phoneNumber,
            "license": license,
            "driverPhoto": driverPhoto,
        },
    )


def tuktuk_allot_3(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    VehicleNumber = request.POST["VehicleNumber"]
    driverID = request.POST["driverID"]
    status = request.POST["status"]
    allotDate = currentDate()

    query = "SELECT * FROM tuktukData WHERE VehicleRegNo = '" + VehicleNumber + "'"
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

    query = (
        "SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData WHERE driverID = '"
        + driverID
        + "'"
    )
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverName = row[1]
        phoneNumber = row[2]
        license = row[3]
        driverPhoto = row[4]

    query = (
        "UPDATE tuktukDriverAllot SET status = 'NO' WHERE VehicleRegNo = '"
        + VehicleNumber
        + "'"
    )
    cursor.execute(query)

    databaseCon.commit()

    query = (
        "UPDATE tuktukDriverAllot SET status = 'NO' WHERE driverID = '" + driverID + "'"
    )
    cursor.execute(query)

    databaseCon.commit()

    query = (
        "SELECT * FROM tuktukDriverAllot WHERE VehicleRegNo = '"
        + VehicleNumber
        + "' AND driverID = '"
        + driverID
        + "'"
    )
    cursor.execute(query)

    existing_record = cursor.fetchone()

    if existing_record:
        msg = (
            "Allotment for " + driverID + " with " + VehicleNumber + " is set to 'NO'."
        )

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

        query = (
            "INSERT INTO tuktukDriverAllot VALUES ('"
            + AllotID
            + "', '"
            + VehicleNumber
            + "', '"
            + driverID
            + "', '"
            + allotDate
            + "', '"
            + status
            + "')"
        )
        cursor.execute(query)

        databaseCon.commit()

        msg = driverID + " Alloted To " + VehicleNumber + " Tuktuk"

    return render(
        request,
        "allotingPage.html",
        {
            "VehicleNumber": VehicleNumber,
            "vehicleType": vehicleType,
            "vehicleFuelType": vehicleFuelType,
            "manufacturedCompany": manufacturedCompany,
            "Vcc": Vcc,
            "year": year,
            " RC": RC,
            "vPhoto": vPhoto,
            "regDate": regDate,
            "driverID": driverID,
            "driverName": driverName,
            "phoneNumber": phoneNumber,
            "license": license,
            "driverPhoto": driverPhoto,
            "VehicleNumber": VehicleNumber,
            "driverID": driverID,
            "allotDate": allotDate,
            "status": status,
            "msg": msg,
        },
    )


def feed_reply(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = (
        "SELECT feedbackID FROM feedback WHERE driverID IS NOT NULL AND reply IS NULL"
    )
    cursor.execute(query)

    records = cursor.fetchall()

    feedbacks = []
    for row in records:
        feedbacks.append(row[0])

    return render(request, "feedReply.html", {"feedbacks": feedbacks})


def user_feedback_reply(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT feedbackID FROM feedback WHERE userID IS NOT NULL AND reply IS NULL"
    cursor.execute(query)

    records = cursor.fetchall()

    userFeedbacks = []

    for row in records:
        userFeedbacks.append(row[0])

    return render(request, "userFeedbackReply.html", {"userFeedbacks": userFeedbacks})


def feed_reply_requests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]

    query = "SELECT * FROM feedback WHERE  feedbackID = '" + feedbackID + "'"
    # print(query̦
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedback = row[1]
        feedbackDate = row[2]
        driverID = row[4]

    query = "SELECT * FROM tuktukDriverData WHERE driverID = '" + driverID + "'"
    # print(query)
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverID = row[0]
        driverName = row[1]
        phoneNumber = row[5]
        license = row[9]
        driverPhoto = row[10]

    return render(
        request,
        "feedbackDetails.html",
        {
            "feedbackID": feedbackID,
            "feedback": feedback,
            "feedbackDate": feedbackDate,
            "driverID": driverID,
            "driverName": driverName,
            "phoneNumber": phoneNumber,
            "license": license,
            "driverPhoto": driverPhoto,
        },
    )


def user_feedback_reply_requests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]

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

    return render(
        request,
        "userFeedbackDetails.html",
        {
            "feedbackID": feedbackID,
            "feedback": feedback,
            "feedbackDate": feedbackDate,
            "userID": userID,
            "userName": userName,
        },
    )


def feedback_details_post(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]
    textarea = request.POST["textarea"]
    replyDate = currentDate()

    query = "SELECT * FROM feedback WHERE  feedbackID = '" + feedbackID + "'"
    # print(query)
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        feedback = row[1]
        feedbackDate = row[2]
        driverID = row[4]

    query = "SELECT * FROM tuktukDriverData WHERE driverID = '" + driverID + "'"
    # print(query)
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    for row in driverRecords:
        driverID = row[0]
        driverName = row[1]
        phoneNumber = row[5]
        license = row[9]
        driverPhoto = row[10]

    query = (
        "UPDATE feedback SET reply = '"
        + textarea
        + "', replyDate = '"
        + replyDate
        + "' WHERE feedbackID = '"
        + feedbackID
        + "'"
    )
    cursor.execute(query)

    databaseCon.commit()

    msg = "Replied.."

    return render(
        request,
        "feedbackDetails.html",
        {
            "feedbackID": feedbackID,
            "feedback": feedback,
            "feedbackDate": feedbackDate,
            "driverID": driverID,
            "driverName": driverName,
            "phoneNumber": phoneNumber,
            "license": license,
            "driverPhoto": driverPhoto,
            "msg": msg,
        },
    )


def tuktuk_for_driver(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT VehicleRegNo FROM tuktukDriverAllot"
    cursor.execute(query)

    records = cursor.fetchall()

    query = "SELECT VehicleRegNo FROM tuktukDriverAllot WHERE status = 'YES'"
    cursor.execute(query)
    # print(query)

    records = cursor.fetchall()

    vehicleList = []

    for row in records:
        vehicleList.append(row[0])

    return render(request, "tuktukForDriver.html", {"vehicleList": vehicleList})


def tuktuk_for_driver_details(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    vehicleNumber = request.POST["vehicleNumber"]
    # print(vehicleNumber)

    query = (
        "SELECT * from tuktukDriverAllot where VehicleRegNo = '"
        + vehicleNumber
        + "' AND status = 'YES'"
    )
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

    query = (
        "SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData WHERE VehicleRegNo = '"
        + vehicleNumber
        + "'"
    )
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

    return render(
        request,
        "tuktukForDriverDetails.html",
        {
            "vehicleNumber": vehicleNumber,
            "vehicleType": vehicleType,
            "vehicleFuelType": vehicleFuelType,
            "manufacturedCompany": manufacturedCompany,
            "Vcc": Vcc,
            "manufactureYear": manufactureYear,
            "RC": RC,
            "vPhoto": vPhoto,
            "regDate": regDate,
            "driverID": driverID,
            "driverName": driverName,
            "phoneNumber": phoneNumber,
            "license": license,
            "driverPhoto": driverPhoto,
        },
    )


def driver_for_tuktuk(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData"
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    return render(request, "driverForTuktuk.html", {"driverRecords": driverRecords})


def driver_for_tuktuk_details(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    driverID = request.POST["driverID"]

    query = (
        "SELECT status, VehicleRegNo FROM tuktukDriverAllot WHERE driverID = '"
        + driverID
        + "' AND status = 'YES' AND VehicleRegNo IN (SELECT VehicleRegNo FROM tuktukDriverAllot WHERE status = 'YES')"
    )
    cursor.execute(query)

    records = cursor.fetchall()

    if not records:
        message = "This driver is not alloted any TukTuk"
        return render(request, "driverForTuktukDetails.html", {"message": message})

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

    query = (
        "SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData WHERE VehicleRegNo = '"
        + VehicleRegNo
        + "'"
    )
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

    return render(
        request,
        "driverForTuktukDetails.html",
        {
            "status": status,
            "VehicleRegNo": VehicleRegNo,
            "vehicleType": vehicleType,
            "vehicleFuelType": vehicleFuelType,
            "manufacturedCompany": manufacturedCompany,
            "Vcc": Vcc,
            "manufactureYear": manufactureYear,
            "RC": RC,
            "vPhoto": vPhoto,
            "regDate": regDate,
            "driverID": driverID,
            "driverName": driverName,
            "phoneNumber": phoneNumber,
            "license": license,
            "driverPhoto": driverPhoto,
        },
    )


def user_list(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT userID, userName, dateOfRegistration FROM tuktukUserData"
    cursor.execute(query)

    records = cursor.fetchall()

    return render(request, "userList.html", {"records": records})


def tuktuk_details(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT VehicleRegNo, vehicleType, vehicleFuelType, manufacturedCompany, Vcc, manufactureYear, RC, vPhoto, regDate FROM tuktukData"
    cursor.execute(query)

    records = cursor.fetchall()

    query = "SELECT driverID, driverName, phoneNumber, license, driverPhoto FROM tuktukDriverData"
    cursor.execute(query)

    driverRecords = cursor.fetchall()

    return render(
        request,
        "tuktukDetails.html",
        {"records": records, "driverRecords": driverRecords},
    )


def fare_estimation(request):
    return render(request, "fareEstimation.html")


def fare_estimation_requests(request):

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

    query = (
        "INSERT INTO fareEstimation VALUES ('"
        + str(fareNO)
        + "', '"
        + minFare
        + "', '"
        + farePerKm
        + "', '"
        + WaitingCharges
        + "', '"
        + currentDateOfChange
        + "', '"
        + MinimumKM
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    message = "New fare details submitted..."

    return render(request, "fareEstimation.html", {"message": message})
