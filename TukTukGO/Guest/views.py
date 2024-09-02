from os import path

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from TukTukGO import connectdb, currentDate
from User.models import loginCredentials, loginSession


# Create your views here.
def home_page(request):  # Home page of TukTukGo
    return render(request, "index.html")


def sign_up_page(request):  # Common SignUp page for Admin, Drivers, and Users
    return render(request, "signUp.html")


def validate_login(request):
    # Retrieve the userID, EMail, and password from the POST request
    userID = request.POST["userID"]
    EMail = request.POST["EMail"]
    password = request.POST["password"]

    # Query the database to find the user with matching credentials
    user = loginCredentials.objects.filter(
        Q(userID=userID) & Q(EMail=EMail) & Q(password=password)
    ).first()

    # If no matching user is found, return an error message
    if user is None:
        msg = "Invalid E-Mail or Password \n Please Try Again"
        return render(request, "signUp1.html", {"msg": msg})

    # Handle login for Admin user
    elif userID == "Admin":
        # Delete any existing login session for the Admin
        loginSession.objects.filter(userType="Admin").delete()

        # Create a new session for the Admin
        loginSession.objects.create(userID=userID, userType="Admin")

        # Set session cookies and redirect to the admin index page
        request.session["userID"] = userID
        request.session["userType"] = "Admin"
        response = render(request, "adminIndex.html")
        response.set_cookie("userID", userID, max_age=31536000, httponly=True)
        return response

    else:
        # Determine if the user is a Driver or a regular User based on userID
        user_type = None
        if userID[0].lower() == "d":
            user_type = "D"
        elif userID[0].lower() == "u":
            user_type = "U"

        if user_type:
            # Delete any existing login session for the determined user type
            loginSession.objects.filter(userType=user_type).delete()

            # Create a new login session for the user
            loginSession.objects.create(userID=userID, userType=user_type)

            # Set session cookies and redirect to the appropriate index page
            request.session["userID"] = userID
            request.session["userType"] = user_type
            if user_type == "D":
                response = render(request, "driverIndex.html")
            else:
                response = render(request, "userIndex.html")
            response.set_cookie(
                "userID",
                userID,
                max_age=31536000,
                httponly=True,
                path="/",
                samesite="Lax",
            )
            return response

        return HttpResponse("User Not Found!")


def log_out(request):
    request.session.flush()

    return redirect("sign_up_page")


def tuktuk_user_login(request):
    return render(request, "tuktukUserLogin.html")


def tuktuk_user_login_requests(request):

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

    query = (
        "INSERT INTO tuktukUserData VALUES('"
        + userID
        + "', '"
        + userName
        + "', '"
        + DateOfRegistration
        + "') "
    )
    cursor.execute(query)

    databaseCon.commit()

    query = (
        "INSERT INTO loginCredentials VALUES('"
        + userID
        + "', '"
        + email
        + "', '"
        + passBox1
        + "')"
    )
    cursor.execute(query)

    databaseCon.commit()

    msg = " User Login Successful \n your userID is " + userID

    return render(request, "tuktukUserLogin.html", {"msg": msg})
