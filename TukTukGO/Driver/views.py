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
def sign_up_page(request):
    return render(request, "signUp.html")


def driver_process(request):
    return render(request, "driverProcess.html")


def driver_change_pass(request):
    return render(request, "driverChangePass.html")


def driver_change_pass_1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    oldPassword = request.POST["t1"]
    newPassword = request.POST["t2"]

    query = "SELECT * FROM loginSession WHERE userType = 'D' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = (
        "SELECT * FROM loginCredentials WHERE UserID = '"
        + driverID
        + "' AND password = '"
        + oldPassword
        + "'"
    )
    cursor.execute(query)

    if cursor.rowcount == 0:
        msg = "Invalid Existing Password"

    else:
        query = (
            "UPDATE loginCredentials SET password = '"
            + newPassword
            + "' WHERE UserID = '"
            + driverID
            + "'"
        )
        cursor.execute(query)

        databaseCon.commit()

        msg = "Password Updated Successfully"

    return render(request, "driverChangePass.html", {"msg": msg})


def feedback(request):
    return render(request, "feedback.html")


def feedback_1(request):

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

    query = (
        "INSERT INTO feedback (feedbackID, feedback, feedbackDate, driverID, name, email) VALUES ('"
        + str(feedbackID)
        + "', '"
        + feedArea
        + "', '"
        + feedbackDate
        + "', '"
        + driverID
        + "', '"
        + name
        + "', '"
        + email
        + "')"
    )
    # print(query)
    cursor.execute(query)

    databaseCon.commit()

    return render(
        request,
        "feedback.html",
        {
            "feedbackID": feedbackID,
            "feedArea": feedArea,
            "feedbackDate": feedbackDate,
            "driverID": driverID,
            "name": name,
            "email": email,
        },
    )


def response_for_tuktuk(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT * FROM loginSession WHERE userType = 'D' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = (
        'SELECT * FROM tuktukRequest WHERE driverID = "'
        + driverID
        + '" AND requestID NOT IN (SELECT requestID FROM tuktukResponse)'
    )
    cursor.execute(query)

    records = cursor.fetchall()

    if cursor.rowcount == 0:
        msg = "No Requests"
        return render(request, "noResponseForTuktuk.html", {"msg": msg})

    else:

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

        return render(
            request,
            "responseForTuktuk.html",
            {
                "requestID": requestID,
                "userName": userName,
                "driverID": driverID,
                "userLat": userLat,
                "userLon": userLon,
                "destination": destination,
            },
        )


def response_for_tuktuk_requests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    requestID = request.POST["requestID"]
    response = request.POST["response"]

    responseTime = time.strftime("%H:%M:%S")
    responseDate = currentDate()

    query = "SELECT * FROM loginSession WHERE userType = 'D' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        driverID = row[0]

    query = (
        'SELECT * FROM tuktukRequest WHERE driverID = "'
        + driverID
        + '" AND requestID NOT IN (SELECT requestID FROM tuktukResponse)'
    )
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

    query = (
        "INSERT INTO tuktukResponse VALUES ('"
        + requestID
        + "', '"
        + responseTime
        + "', '"
        + responseDate
        + "', '"
        + response
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    message = "Response Submitted"

    return render(
        request,
        "responseForTuktuk.html",
        {
            "requestID": requestID,
            "userName": userName,
            "driverID": driverID,
            "userLat": userLat,
            "userLon": userLon,
            "destination": destination,
            "message": message,
        },
    )


def receipt(request):
    return render(request, "receipt.html")


def receipt_requests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    totalDistance = request.POST["totalDistance"]
    print(totalDistance)
    waitingCharge = request.POST["waitingCharge"]

    emotionFeedback = request.POST["emotionFeedback"]

    endOfRideDate = currentDate()
    endOfRideTime = time.strftime("%H:%M:%S")

    query = "SELECT * FROM fareEstimation ORDER BY fareNO desc"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        minimumFare = row[1]
        farePerKm = row[2]
        waitingFare = row[3]
        minimumKM = row[5]

    if float(totalDistance) <= minimumKM:
        fare = minimumFare
    else:
        fareMinKM = float(totalDistance) - minimumKM
        fareMinKMperKm = fareMinKM * farePerKm
        fare = minimumFare + fareMinKMperKm

    wcmin = waitingFare / 60

    if int(waitingCharge) >= 10:
        wcCharge = wcmin * int(waitingCharge)
    else:
        wcCharge = 0

    totalRideRate = fare + wcCharge

    query = "SELECT requestID FROM tuktukResponse ORDER BY requestID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]
        break

    query = (
        "INSERT INTO endOfRide (requestID, totalRideRate, waitingCharges, endOfRideDate, endOfRideTime, totalDistance, emotionFeedback) VALUES('"
        + requestID
        + "', '"
        + str(totalRideRate)
        + "', '"
        + waitingCharge
        + "', '"
        + endOfRideDate
        + "', '"
        + endOfRideTime
        + "', '"
        + totalDistance
        + "', '"
        + emotionFeedback
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    return render(
        request,
        "receipt.html",
        {
            "requestID": requestID,
            "totalRideRate": totalRideRate,
            "totalDistance": totalDistance,
            "waitingCharge": waitingCharge,
            "endOfRideDate": endOfRideDate,
            "endOfRideTime": endOfRideTime,
            "emotionFeedback": emotionFeedback,
        },
    )


def receipt_requests_confirm(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT requestID FROM endOfRide ORDER BY requestID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]
        break

    query = "SELECT * FROM endOfRide ORDER BY requestID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        totalDistance = row[6]
        totalRideRate = row[1]
        waitingCharges = row[2]
        emotionFeedback = row[5]
        endOfRideDate = row[3]
        endOfRideTime = row[4]

    message = "Thank You! For The ride"
    return render(
        request,
        "receiptRequestsConfirm.html",
        {
            "requestID": requestID,
            "totalDistance": totalDistance,
            "totalRideRate": totalRideRate,
            "waitingCharges": waitingCharges,
            "emotionFeedback": emotionFeedback,
            "endOfRideDate": endOfRideDate,
            "endOfRideTime": endOfRideTime,
            "message": message,
        },
    )


def on_going_ride(request):
    return render(request, "onGoingRide.html")


def on_going_ride_requests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    minFare = request.POST["minFare"]
    WaitingCharges = request.POST["WaitingCharges"]
    comment = request.POST["comment"]

    onGoingRideDate = currentDate()
    onGoingRideTime = time.strftime("%H:%M:%S")

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

    query = (
        "INSERT INTO onGoingRide VALUES ('"
        + requestID
        + "', '"
        + minFare
        + "', '"
        + WaitingCharges
        + "', '"
        + onGoingRideDate
        + "', '"
        + onGoingRideTime
        + "', '"
        + comment
        + "') "
    )
    cursor.execute(query)

    databaseCon.commit()

    message = "Ride Completed! Thank You!!"

    return render(request, "onGoingRide.html", {"message": message})


def map_view(request):

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
    driver_data.append(
        {
            "vehicleRegNo": vehicleRegNo,
            "latitude": tuktukLatitude,
            "longitude": tuktukLongitude,
        }
    )

    user_data = []
    for record in user_records:
        userID = record[0]
        userLat = float(record[1])
        userLon = float(record[2])
        destination = record[3]

    user_data.append(
        {
            "userID": userID,
            "latitude": userLat,
            "longitude": userLon,
            "destination": destination,
        }
    )

    return render(
        request,
        "mapView.html",
        {"driver_data": driver_data, "user_data": user_data},
    )


def driver_ride_details(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    requestID = request.POST["requestID"]
    totalDistance = request.POST["totalDistance"]
    waitingCharge = request.POST["waitingCharge"]

    query = "SELECT * FROM fareEstimation ORDER BY fareNO desc"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        minimumFare = row[1]
        farePerKm = row[2]
        waitingFare = row[3]
        minimumKM = row[5]

    if float(totalDistance) <= minimumKM:
        fare = minimumFare
    else:
        fareMinKM = float(totalDistance) - minimumKM
        fareMinKMperKm = fareMinKM * farePerKm
        fare = minimumFare + fareMinKMperKm

    wcmin = waitingFare / 60

    if int(waitingCharge) >= 10:
        wcCharge = wcmin * int(waitingCharge)
    else:
        wcCharge = 0

    totalRideRate = fare + wcCharge

    query = "SELECT requestID FROM tuktukResponse ORDER BY requestID DESC"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        requestID = row[0]
        break

    return render(
        request,
        "driverRideDetails.html",
        {
            "requestID": requestID,
            "waitingCharge": waitingCharge,
            "totalDistance": totalDistance,
        },
    )
