from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from TukTukGO import connectdb, currentDate


# Create your views here.
def home_page(request):  # Home page of TukTukGo
    return render(request, "index.html")


def sign_up_page(request):  # Common SignUp page for Admin, Drivers, and Users
    return render(request, "signUp.html")


def validate_login(
    request,
):  # This function validates the login credentials and redirects to their page

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    userID = request.POST["userID"]
    EMail = request.POST["EMail"]
    password = request.POST["password"]

    query = "SELECT * FROM loginCredentials WHERE UserID = %s AND EMail = %s AND password = %s"
    cursor.execute(query, (userID, EMail, password))

    if cursor.rowcount == 0:

        msg = "Invalid E-Mail or Password \n Please Try Again"

        return render(request, "signUp1.html", {"msg": msg})

    elif userID == "Admin":

        query = "DELETE FROM loginSession WHERE userType = %s"
        cursor.execute(query, ("Admin",))

        databaseCon.commit()

        query = "INSERT INTO loginSession (userID, userType) VALUES (%s, %s)"
        cursor.execute(query, (userID, "Admin"))

        databaseCon.commit()

        response = render(request, "adminIndex.html")
        response.set_cookie("userID", userID, httponly=True)
        return response

    else:

        x = userID[0]

        if x == "D" or x == "d":

            query = "DELETE FROM loginSession WHERE userType = %s"
            cursor.execute(query, ("D",))

            databaseCon.commit()

            query = "INSERT INTO loginSession (userID, userType) VALUES (%s, %s)"
            cursor.execute(query, (userID, "D"))

            databaseCon.commit()

            response = render(request, "driverIndex.html")
            response.set_cookie("userID", userID, httponly=True)
            return response

        elif x == "U" or x == "u":

            query = "DELETE FROM loginSession WHERE userType = %s"
            cursor.execute(query, ("U",))

            databaseCon.commit()

            query = "INSERT INTO loginSession (userID, userType) VALUES (%s, %s)"
            cursor.execute(query, (userID, "U"))

            databaseCon.commit()

            response = render(request, "userIndex.html")
            response.set_cookie("userID", userID, httponly=True)
            return response

        return HttpResponse("User Not Found!")


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


def fare_data(request):

    databaseCon = connectdb()
    cursor = databaseCon.cursor()

    query = "SELECT * FROM fareEstimation ORDER BY fareNO DESC "
    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]  # Get column names
    data = [dict(zip(columns, row)) for row in rows]

    return JsonResponse(data, safe=False)

def privacy_conditions(request):
    return render (request, "privacy_conditions.html")
