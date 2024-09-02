from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from Driver.models import endOfRide
from Guest.models import tuktukUserData
from TukTukGO import connectdb, currentDate
from User.models import loginCredentials

from .models import (
    fareEstimation,
    feedback,
    tuktukData,
    tuktukDriverAllot,
    tuktukDriverData,
)

# Create your views here.


def sign_up_page(request):
    return render(request, "signUp.html")


def admin_process(request):

    databaseCon = connectdb()

    try:

        total_bookings = endOfRide.objects.count()
        total_money = (
            endOfRide.objects.aggregate(total=Sum("totalRideRate"))["total"] or 0
        )
    finally:
        databaseCon.close()

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

    s1 = request.POST["t1"]
    s2 = request.POST["t2"]

    try:
        user = loginCredentials.objects.get(userID="Admin", password=s1)
    except loginCredentials.DoesNotExist:
        msg = "Incorrect Existing Password"

    else:

        user.password = s2
        user.save()
        msg = "Password Updated Successfully"

    return render(request, "changePass.html", {"msg": msg})


def tuktuk_registration(request):
    return render(request, "tuktukRegistration.html")


def tuktuk_registration_1(request):

    vehicle_number = request.POST["vehicle_number"]
    vehicle_type = request.POST["vehicle_type"]
    fuel_type = request.POST["fuel_type"]
    manufactured_company = request.POST["manufactured_company"]
    vehicle_cc = request.POST["vehicle_cc"]
    year = request.POST["year"]
    rc_upload = request.FILES["rc_upload"]
    vehicle_photo = request.FILES["vehicle_photo"]
    date_of_registration = request.POST["date_of_registration"]

    fs = FileSystemStorage()
    rc_upload_name = fs.save(
        "static/data/tuktukProof/dataProof/" + rc_upload.name, rc_upload
    )
    rc_upload_name = rc_upload_name[34:]
    vehicle_photo_name = fs.save(
        "static/data/tuktukProof/dataProof/" + vehicle_photo.name, vehicle_photo
    )
    vehicle_photo_name = vehicle_photo_name[34:]

    if tuktukData.objects.filter(VehicleRegNo=vehicle_number).exists():
        msg = "Tuktuk Registration Already Exists"

    else:
        new_tuktuk = tuktukData(
            VehicleRegNo=vehicle_number,
            vehicleType=vehicle_type,
            vehicleFuelType=fuel_type,
            manufacturedCompany=manufactured_company,
            Vcc=vehicle_cc,
            manufactureYear=year,
            RC=rc_upload_name[34:],
            vPhoto=vehicle_photo_name[34:],
            regDate=date_of_registration,
        )
        new_tuktuk.save()
        msg = "Tuktuk Registration Successful"

    return render(request, "TukTukRegistration.html", {"msg": msg})


def tuktuk_driver_registration(request):
    return render(request, "driverRegistration.html")


def tuktuk_driver_registration_1(request):

    driver_name = request.POST["driver_name"]
    house_name = request.POST["house_name"]
    place_name = request.POST["place_name"]
    pincode = request.POST["pincode"]
    email = request.POST["email"]
    phone_number = request.POST["phone_number"]
    driver_gender = request.POST["driver_gender"]
    driver_gender = request.POST["driver_gender"]
    dob = request.POST["dob"]
    aadhar = request.POST["aadhar"]
    license = request.POST["license"]
    driver_photo = request.FILES["driver_photo"]
    date_of_registration = request.POST["date_of_registration"]

    fs = FileSystemStorage()
    driver_photo_proof = fs.save(
        "static/data/tuktukProof/dataProof/" + driver_photo.name, driver_photo
    )
    driver_photo_proof = driver_photo_proof[34:]

    last_driver = tuktukDriverData.objects.order_by("-driverID").first()

    if last_driver:

        last_id = int(last_driver.driverID[1:])
        new_driverID = f"D{last_id + 1}"

    else:

        new_driverID = "D1000"

    new_driver = tuktukDriverData(
        driverID=new_driverID,
        driverName=driver_name,
        houseName=house_name,
        placeName=place_name,
        pincode=pincode,
        phoneNumber=phone_number,
        gender=driver_gender,
        dateOfBirth=dob,
        aadhar=aadhar,
        license=license,
        driverPhoto=driver_photo,
        dateOfRegistration=date_of_registration,
    )

    new_driver.save()

    new_driver_login_credentials = loginCredentials(
        userID=new_driverID,
        EMail=email,
        password=new_driverID,
    )

    new_driver_login_credentials.save()

    msg = f"Driver Registration Successfully Finished\n Default Password is your DriverID is {new_driverID}"

    return render(request, "driverRegistration.html", {"msg": msg})


def tuktuk_allot(request):

    vehicle_list = tuktukData.objects.values_list("VehicleRegNo", flat=True)

    return render(
        request,
        "tuktukAllot.html",
        {"vehicle_list": vehicle_list},
    )


def tuktuk_allot_1(request):

    vehicle_number = request.POST["vehicle_number"]

    records = tuktukData.objects.filter(VehicleRegNo=vehicle_number).values(
        "VehicleRegNo",
        "vehicleType",
        "vehicleFuelType",
        "manufacturedCompany",
        "Vcc",
        "manufactureYear",
        "RC",
        "vPhoto",
        "regDate",
    )
    driver_records = tuktukDriverData.objects.all()

    return render(
        request,
        "allotDetails.html",
        {
            "vehicle_number": vehicle_number,
            "records": records,
            "driver_records": driver_records,
        },
    )


def tuktuk_allot_2(request):

    vehicle_number = request.POST["vehicle_number"]
    driverID = request.POST["driverID"]

    tuktuk = get_object_or_404(tuktukData, VehicleRegNo=vehicle_number)

    driver = get_object_or_404(tuktukDriverData, driverID=driverID)
    return render(
        request,
        "allotingPage.html",
        {
            "vehicle_number": tuktuk.VehicleRegNo,
            "vehicleType": tuktuk.vehicleType,
            "vehicleFuelType": tuktuk.vehicleFuelType,
            "manufacturedCompany": tuktuk.manufacturedCompany,
            "Vcc": tuktuk.Vcc,
            "year": tuktuk.manufactureYear,
            " RC": tuktuk.RC,
            "vPhoto": tuktuk.vPhoto,
            "regDate": tuktuk.regDate,
            "driverID": driver.driverID,
            "driverName": driver.driverName,
            "phoneNumber": driver.phoneNumber,
            "license": driver.license,
            "driverPhoto": driver.driverPhoto,
        },
    )


def tuktuk_allot_3(request):

    vehicle_number = request.POST["vehicle_number"]
    driverID = request.POST["driverID"]
    status = request.POST["status"]
    allot_date = currentDate()

    tuktuk = get_object_or_404(tuktukData, VehicleRegNo=vehicle_number)

    driver = get_object_or_404(tuktukDriverData, driverID=driverID)

    tuktukDriverAllot.objects.filter(VehicleRegNo=vehicle_number).update(status="NO")
    tuktukDriverAllot.objects.filter(driverID=driverID).update(status="NO")

    existing_allotment_check = tuktukDriverAllot.objects.filter(
        VehicleRegNo=vehicle_number, driverID=driverID
    ).first()

    if existing_allotment_check:
        msg = f"Allotment for {driverID} with {vehicle_number} is set to 'NO'."
    else:
        new_allotment = tuktukDriverAllot.objects.order_by("-allotID").first()
        if new_allotment:
            new_ID = int(new_allotment.allotID[3:]) + 1
            allotID = f"A{new_ID}"
        else:
            allotID = "A1000"

        new_allocation = tuktukDriverAllot.objects.create(
            allotID=allotID,
            VehicleRegNo=vehicle_number,
            driverID=driverID,
            allotDate=allot_date,
            status="YES",
        )
        msg = f"{driverID} is alloted to {vehicle_number} Tuktuk."

    return render(
        request,
        "allotingPage.html",
        {
            "vehicle_number": vehicle_number,
            "vehicleType": tuktuk.vehicleType,
            "vehicleFuelType": tuktuk.vehicleFuelType,
            "manufacturedCompany": tuktuk.manufacturedCompany,
            "Vcc": tuktuk.Vcc,
            "year": tuktuk.manufactureYear,
            " RC": tuktuk.RC,
            "vPhoto": tuktuk.vPhoto,
            "regDate": tuktuk.regDate,
            "driverID": driver.driverID,
            "driverName": driver.driverName,
            "phoneNumber": driver.phoneNumber,
            "license": driver.license,
            "driverPhoto": driver.driverPhoto,
            "allotDate": allot_date,
            "status": status,
            "msg": msg,
        },
    )


def feed_reply(request):

    feedback_list = feedback.objects.filter(
        driverID__isnull=False, reply__isnull=True
    ).values_list("feedbackID", flat=True)

    return render(request, "feedReply.html", {"feedback_list": feedback_list})


def user_feedback_reply(request):

    user_feedback_list = feedback.objects.filter(
        userID__isnull=False, reply__isnull=True
    ).values_list("feedbackID", flat=True)

    return render(
        request, "userFeedbackReply.html", {"user_feedback_list": user_feedback_list}
    )


def feed_reply_requests(request):

    feedbackID = request.POST["feedbackID"]

    feedback_records = get_object_or_404(feedback, feedbackID=feedback)

    driver_records = get_object_or_404(
        tuktukDriverData, driverID=feedback_records.driverID
    )
    return render(
        request,
        "feedbackDetails.html",
        {
            "feedbackID": feedbackID,
            "feedback": feedback_records.feedback,
            "feedbackDate": feedback_records.feedbackDate,
            "driverID": driver_records.driverID,
            "driverName": driver_records.driverName,
            "phoneNumber": driver_records.phoneNumber,
            "license": driver_records.license,
            "driverPhoto": driver_records.driverPhoto,
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

    tuktuks = tuktukDriverAllot.objects.filter(status="YES").values_list(
        "VehicleRegNo", flat=True
    )

    tuktuk_list = list(tuktuks)

    return render(request, "tuktukForDriver.html", {"tuktuk_list": tuktuk_list})


def tuktuk_for_driver_details(request):

    vehicle_number = request.POST["vehicle_number"]

    alloted_tuktuk = get_object_or_404(
        tuktukDriverAllot, VehicleRegNo=vehicle_number, status="YES"
    )

    driver_details = get_object_or_404(
        tuktukDriverData, driverID=alloted_tuktuk.driverID
    )

    tuktuk = get_object_or_404(tuktukData, VehicleRegNo=vehicle_number)

    return render(
        request,
        "tuktukForDriverDetails.html",
        {
            "vehicle_number": vehicle_number,
            "vehicleType": tuktuk.vehicleType,
            "vehicleFuelType": tuktuk.vehicleFuelType,
            "manufacturedCompany": tuktuk.manufacturedCompany,
            "Vcc": tuktuk.Vcc,
            "manufactureYear": tuktuk.manufactureYear,
            "RC": tuktuk.RC,
            "vPhoto": tuktuk.vPhoto,
            "regDate": tuktuk.regDate,
            "driverID": driver_details.driverID,
            "driverName": driver_details.driverName,
            "phoneNumber": driver_details.phoneNumber,
            "license": driver_details.license,
            "driverPhoto": driver_details.driverPhoto,
        },
    )


def driver_for_tuktuk(request):

    driver_details = tuktukDriverData.objects.all()

    return render(request, "driverForTuktuk.html", {"driver_details": driver_details})


def driver_for_tuktuk_details(request):

    driverID = request.POST["driverID"]

    try:
        alloted_tuktuk = tuktukDriverAllot.objects.get(driverID=driverID, status="YES")

        driver_details = get_object_or_404(tuktukDriverData, driverID=driverID)

        tuktuk_details_else = get_object_or_404(
            tuktukData, VehicleRegNo=alloted_tuktuk.VehicleRegNo
        )

        return render(
            request,
            "driverForTuktukDetails.html",
            {
                "status": alloted_tuktuk.status,
                "VehicleRegNo": tuktuk_details_else.VehicleRegNo,
                "vehicleType": tuktuk_details_else.vehicleType,
                "vehicleFuelType": tuktuk_details_else.vehicleFuelType,
                "manufacturedCompany": tuktuk_details_else.manufacturedCompany,
                "Vcc": tuktuk_details_else.Vcc,
                "manufactureYear": tuktuk_details_else.manufactureYear,
                "RC": tuktuk_details_else.RC,
                "vPhoto": tuktuk_details_else.vPhoto,
                "regDate": tuktuk_details_else.regDate,
                "driverID": driver_details.driverID,
                "driverName": driver_details.driverName,
                "phoneNumber": driver_details.phoneNumber,
                "license": driver_details.license,
                "driverPhoto": driver_details.driverPhoto,
            },
        )

    except tuktukDriverAllot.DoesNotExist:
        message = "This driver is not alloted to any Tuktuk."
        return render(request, "driverForTuktukDetails.html", {"message": message})


def user_list(request):

    records = tuktukUserData.objects.values("userID", "userName", "dateOfRegistration")

    return render(request, "userList.html", {"records": records})


def tuktuk_details(request):

    tuktuk_details = tuktukData.objects.all()

    driver_details = tuktukDriverData.objects.all()

    return render(
        request,
        "tuktukDetails.html",
        {"tuktuk_details": tuktuk_details, "driver_details": driver_details},
    )


def fare_estimation(request):

    return render(request, "fareEstimation.html")


def fare_estimation_requests(request):

    new_fare = fareEstimation.objects.order_by("-fareNO").first()
    fareNO = (new_fare.fareNO + 1) if new_fare else 1

    min_fare = request.POST.get("min_fare")
    fare_per_km = request.POST.get("fare_per_km")
    waiting_charges = request.POST.get("waiting_charges")
    minimum_km = request.POST.get("minimum_km")

    new_fare_estimation = fareEstimation(
        fareNO=fareNO,
        minimumFare=min_fare,
        farePerKm=fare_per_km,
        waitingFare=waiting_charges,
        currentDateOfChange=timezone.now(),
        minimumKM=minimum_km,
    )
    new_fare_estimation.save()

    message = "New fare details submitted..."

    return render(request, "fareEstimation.html", {"message": message})
