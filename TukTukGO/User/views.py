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


def user_process(request):
    return render(request, "userProcess.html")


def user_change_pass(request):
    return render(request, "userChangePass.html")


def user_change_pass_1(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    oldPassword = request.POST["t1"]
    newPassword = request.POST["t2"]

    query = "SELECT * FROM loginSession WHERE userType = 'U' "
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        userID = row[0]

    query = (
        "SELECT * FROM loginCredentials WHERE UserID = '"
        + userID
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
            + userID
            + "'"
        )
        cursor.execute(query)

        databaseCon.commit()

        msg = "Password Updated Successfully"

    return render(request, "userChangePass.html", {"msg": msg})


def user_feedback(request):
    return render(request, "userfeedback.html")


def user_feedback_1(request):

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

    query = (
        "INSERT INTO feedback (feedbackID, feedback, feedbackDate, userID, name, email) VALUES ('"
        + str(feedbackID)
        + "', '"
        + feedArea
        + "', '"
        + feedbackDate
        + "', '"
        + userID
        + "', '"
        + name
        + "', '"
        + email
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    return render(
        request,
        "userFeedback.html",
        {
            "feedbackID": feedbackID,
            "feedArea": feedArea,
            "feedbackDate": feedbackDate,
            "userID": userID,
            "name": name,
            "email": email,
        },
    )


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


def user_feedback_details_post(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    feedbackID = request.POST["feedbackID"]
    textarea = request.POST["textarea"]
    replyDate = currentDate()

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

    message = "Replied.."

    return render(
        request,
        "userFeedbackDetails.html",
        {
            "feedbackID": feedbackID,
            "feedback": feedback,
            "feedbackDate": feedbackDate,
            "userID": userID,
            "userName": userName,
            "message": message,
        },
    )


# List of auto locations


def request_tuktuk_and_tuktuk_driver(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    userLat = request.POST["userLat"]
    userLon = request.POST["userLon"]

    nearestAutoID = request.POST["nearestAutoID"]

    destCoordinates = request.POST["destCoordinates"]

    requestDate = currentDate()
    requestTime = time.strftime("%H:%M:%S")

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

    query = (
        "SELECT * FROM tuktukDriverAllot WHERE VehicleRegNo = '"
        + nearestAutoID
        + "' AND status = 'YES'"
    )
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

    query = (
        "INSERT INTO tuktukRequest VALUES ('"
        + requestID
        + "', '"
        + userID
        + "', '"
        + destCoordinates
        + "' ,'"
        + requestDate
        + "', '"
        + requestTime
        + "', '"
        + nearestAutoID
        + "', '"
        + userLat
        + "', '"
        + userLon
        + "', '"
        + driverID
        + "', '"
        + distance
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    return redirect("ride_details")


def booking_page(request):
    return render(request, "bookingPage.html")


auto_locations = [
    {"id": "KL01B4346", "lat": 9.152091, "lon": 76.738282},
    {"id": "KL05L6452", "lat": 9.154538, "lon": 76.732662},
    {"id": "KL23A6767", "lat": 9.132163, "lon": 76.768493},
    {"id": "KL65J9284", "lat": 9.149356, "lon": 76.755677},
]

ids = [auto["id"] for auto in auto_locations]
first_id = ids[0]

# print(first_id)

logger = logging.getLogger(__name__)


def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

    headers = {
        "User-Agent": "mapping (adithyanprdev@gmail.com)"  # Replace with your application name and contact information
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("display_name")


# Function to connect to the MySQL database and fetch fare estimation parameters
def get_fare_parameters():
    try:
        databaseCon = connectdb()
        cursor = databaseCon.cursor()

        query = "SELECT minimumFare, farePerKm, waitingFare, minimumKM FROM fareEstimation ORDER BY fareNO DESC"
        cursor.execute(query)
        result = (
            cursor.fetchone()
        )  # Fetch one row as we only need the latest fare parameters

        if result:
            fare_params = {
                "minimumFare": float(result[0]),
                "farePerKm": float(result[1]),
                "waitingFare": float(result[2]),
                "minimumKM": float(result[3]),
            }
            print("Fare Parameters: ", fare_params)  # Debug statement
            return fare_params
        else:
            raise Exception("Fare estimation parameters not found")
    finally:
        databaseCon.close()


def calculate_fare(distance, fare_params):
    if distance <= fare_params["minimumKM"]:
        return fare_params["minimumFare"]
    else:
        return (
            fare_params["minimumFare"]
            + (distance - fare_params["minimumKM"]) * fare_params["farePerKm"]
        )


@csrf_exempt
def calculate_distance_and_allot_auto(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_lat = float(data.get("user_lat"))
            user_lon = float(data.get("user_lon"))
            dest_name = data.get("dest_name")
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.error("Invalid JSON or missing data: %s", e)
            return JsonResponse({"error": "Invalid JSON or missing data"}, status=400)

        api_key = "5b3ce3597851110001cf6248d0882d4d8035451eb97f11ef667f07b1"
        geocode_url = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={dest_name}"

        try:
            geocode_response = requests.get(geocode_url)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()
        except requests.RequestException as e:
            logger.error("Error fetching geocode data: %s", e)
            return JsonResponse(
                {"error": "Error fetching geocode data", "details": str(e)}, status=500
            )

        if "features" not in geocode_data or not geocode_data["features"]:
            logger.error("Destination not found for: %s", dest_name)
            return JsonResponse({"error": "Destination not found"}, status=404)

        destination = geocode_data["features"][0]["geometry"]["coordinates"]
        dest_lon, dest_lat = destination

        # Calculate the distance between user and destination using OpenRouteService
        route_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={user_lon},{user_lat}&end={dest_lon},{dest_lat}"
        try:
            route_response = requests.get(route_url)
            route_response.raise_for_status()
            route_data = route_response.json()
            distance_to_destination = (
                route_data["features"][0]["properties"]["segments"][0]["distance"]
                / 1000
            )  # convert to km
        except requests.RequestException as e:
            logger.error("Error fetching route data: %s", e)
            return JsonResponse(
                {"error": "Error fetching route data", "details": str(e)}, status=500
            )

        min_distance = float("inf")
        nearest_auto = None

        # Finding the nearest auto
        for auto in auto_locations:
            auto_lat = auto["lat"]
            auto_lon = auto["lon"]
            distance = haversine(user_lat, user_lon, auto_lat, auto_lon)

            if distance < min_distance:
                min_distance = distance
                nearest_auto = (
                    auto.copy()
                )  # Make a copy to avoid modifying the original dict

        if nearest_auto:
            nearest_auto["location"] = reverse_geocode(
                nearest_auto["lat"], nearest_auto["lon"]
            )

            # Fetch fare parameters
            try:
                fare_params = get_fare_parameters()
            except Exception as e:
                logger.error("Error fetching fare parameters: %s", e)
                return JsonResponse(
                    {"error": "Error fetching fare parameters", "details": str(e)},
                    status=500,
                )

            # Calculate fare based on distance to destination
            fare = calculate_fare(distance_to_destination, fare_params)

            return JsonResponse(
                {
                    "distance": min_distance,
                    "nearest_auto": nearest_auto,
                    "destination_lat": dest_lat,
                    "destination_lon": dest_lon,
                    "fare_estimation": fare,
                },
                status=200,
            )
        else:
            logger.error("No autos available")
            return JsonResponse({"error": "No autos available"}, status=404)
    else:
        logger.error("Method not allowed")
        return JsonResponse({"error": "Method not allowed"}, status=405)


def haversine(lat1, lon1, lat2, lon2):
    import math

    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def loading(request):
    return render(request, "loading.html")


def check_driver_response(request):
    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    # Fetching requestID from session or POST data
    requestID = request.session.get("requestID")

    # Implement logic to check if the driver has responded
    query = f"SELECT response FROM tuktukResponse WHERE requestID = '{requestID}' ORDER BY responseDate DESC, responseTime DESC LIMIT 1"
    cursor.execute(query)
    response = cursor.fetchone()

    if response and response[0] == "YES":
        # Driver has responded
        return JsonResponse({"response": True})
    else:
        # Driver has not responded yet
        return JsonResponse({"response": False})


def ride_details(request):
    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    if request.method == "POST":
        # Fetch latest details from database
        responseTime = time.strftime("%H:%M:%S")
        responseDate = currentDate()

        # Get driverID from loginSession where userType is 'D'
        query = "SELECT * FROM loginSession WHERE userType = 'D'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            driverID = row[0]

        # Get driver details
        query = (
            "SELECT driverName, driverPhoto FROM tuktukDriverData WHERE driverID = '"
            + driverID
            + "'"
        )
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
        query = (
            "SELECT response, responseTime, responseDate FROM tuktukResponse WHERE requestID = '"
            + requestID
            + "'"
        )
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

        # Initialize VehicleRegNo
        VehicleRegNo = "Not Assigned"

        # Get VehicleRegNo
        query = (
            "SELECT VehicleRegNo FROM tuktukDriverAllot WHERE driverID = '"
            + driverID
            + "' AND status = 'YES'"
        )
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            for row in records:
                VehicleRegNo = row[0]

        message = "You can Identify your Tuktuk & Driver using this Details"

        return render(
            request,
            "rideDetails.html",
            {
                "requestID": requestID,
                "userName": userName,
                "userLat": userLat,
                "userLon": userLon,
                "destination": destination,
                "response": response,
                "responseTime": responseTime,
                "responseDate": responseDate,
                "driverID": driverID,
                "driverPhoto": driverPhoto,
                "driverName": driverName,
                "VehicleRegNo": VehicleRegNo,
                "message": message,
            },
        )

    else:  # GET request
        # Initially load the details
        responseTime = time.strftime("%H:%M:%S")
        responseDate = currentDate()

        # Get driverID from loginSession where userType is 'D'
        query = "SELECT * FROM loginSession WHERE userType = 'D'"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            driverID = row[0]

        # Get driver details
        query = (
            "SELECT driverName, driverPhoto FROM tuktukDriverData WHERE driverID = '"
            + driverID
            + "'"
        )
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
        query = (
            "SELECT response, responseTime, responseDate FROM tuktukResponse WHERE requestID = '"
            + requestID
            + "'"
        )
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

        # Initialize VehicleRegNo
        VehicleRegNo = "Not Assigned"

        # Get VehicleRegNo
        query = (
            "SELECT VehicleRegNo FROM tuktukDriverAllot WHERE driverID = '"
            + driverID
            + "' AND status = 'YES'"
        )
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            for row in records:
                VehicleRegNo = row[0]

        message = "You can Identify your Tuktuk & Driver using this Details"

        return render(
            request,
            "rideDetails.html",
            {
                "requestID": requestID,
                "userName": userName,
                "userLat": userLat,
                "userLon": userLon,
                "destination": destination,
                "response": response,
                "responseTime": responseTime,
                "responseDate": responseDate,
                "driverID": driverID,
                "driverPhoto": driverPhoto,
                "driverName": driverName,
                "VehicleRegNo": VehicleRegNo,
                "message": message,
            },
        )


def payment_history(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT tr.requestID FROM tuktukRequest tr WHERE EXISTS (SELECT 1 FROM loginSession ls WHERE ls.userID = tr.userID AND ls.userType = 'U') AND EXISTS (SELECT 1 FROM endOfRide eor WHERE eor.requestID = tr.requestID)"
    cursor.execute(query)

    records = cursor.fetchall()

    recentRidesList = []

    for row in records:
        recentRidesList.append(row[0])

    query = "SELECT * FROM endOfRide"
    cursor.execute(query)

    records = cursor.fetchall()
    print(records)

    for row in records:
        endOfRideDate = row[3]
        totalRideRate = row[1]

    return render(
        request,
        "paymentHistory.html",
        {
            "recentRidesList": recentRidesList,
            "totalRideRate": totalRideRate,
            "endOfRideDate": endOfRideDate,
        },
    )


def feedback_view(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT feedbackID, feedbackDate FROM feedback"
    cursor.execute(query)

    records = cursor.fetchall()

    recent_feedback_list = []

    for row in records:
        recent_feedback_list.append((row[0], row[1]))
    print(records)

    return render(
        request,
        "feedbackView.html",
        {
            "recent_feedback_list": recent_feedback_list,
        },
    )


def feedback_view_requests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT f.userID from feedback f WHERE EXISTS (SELECT userID FROM loginSession ls WHERE ls.userID = f.userID AND userType = 'U')"
    cursor.execute(query)

    records = cursor.fetchall()

    for row in records:
        userID = row[0]
        break

    # query = "SELECT ls.userID, lc.EMail  FROM loginSession ls  JOIN loginCredentials lc ON ls.userID = lc.userID AND ls.userType = 'Admin';"
    # cursor.execute(query)

    # adminRecords = cursor.fetchall()

    # for row in adminRecords:
    #    adminUserID = row[0]
    #    adminEMail = row[1]
    #    break

    query = "SELECT feedbackID, feedback, feedbackDate, userID, name, EMail, reply, replyDate FROM feedback ORDER BY feedbackID DESC"
    cursor.execute(query)

    records = cursor.fetchall()
    print(records)

    for row in records:
        feedbackID = row[0]
        feedback = row[1]
        feedbackDate = row[2]
        userID = row[3]
        name = row[4]
        EMail = row[5]
        reply = row[6]
        replyDate = row[7]
        break
    print(records)

    return render(
        request,
        "feedbackViewRequests.html",
        {
            "feedback": feedback,
            "feedbackID": feedbackID,
            "feedbackDate": feedbackDate,
            "userID": userID,
            "name": name,
            "EMail": EMail,
            "reply": reply,
            "replyDate": replyDate,
        },
    )

    # def feedback_view_requests(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    # Fetch user feedback records
    query = """
    SELECT feedbackID, feedback, feedbackDate, f.userID, name, lc.EMail, reply, replyDate
    FROM feedback f
    JOIN loginCredentials lc ON f.userID = lc.userID
    WHERE EXISTS (
        SELECT 1 FROM loginSession ls WHERE ls.userID = f.userID AND ls.userType = 'U'
    )
    """
    cursor.execute(query)
    feedback_records = cursor.fetchall()

    records = []
    for row in feedback_records:
        records.append(
            {
                "feedbackID": row[0],
                "feedback": row[1],
                "feedbackDate": row[2],
                "userID": row[3],
                "name": row[4],
                "EMail": row[5],
                "reply": row[6],
                "replyDate": row[7],
            }
        )

    # Fetch admin records
    query = """
    SELECT ls.userID, lc.EMail 
    FROM loginSession ls  
    JOIN loginCredentials lc ON ls.userID = lc.userID 
    WHERE ls.userType = 'Admin'
    """
    cursor.execute(query)
    admin_records = cursor.fetchall()

    admin_records_list = []
    for row in admin_records:
        admin_records_list.append({"adminUserID": row[0], "adminEMail": row[1]})

    # Close the database connection
    cursor.close()
    databaseCon.close()

    return render(
        request,
        "feedbackViewRequests.html",
        {"records": records, "adminRecords": admin_records_list},
    )
