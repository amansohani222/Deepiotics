import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import JsonResponse
from ml import predict
from services.models import Customer


def register(request):
    if request.method == 'POST':
        try:
            Customer.objects.get(email=request.POST['email'])
            return JsonResponse({"message": "Email already exist", "status": -1})
        except Exception:
            c1 = Customer(email=request.POST['email'], name=request.POST['name'], phone=request.POST['phone'],
                          company_name=request.POST['company_name'])
            verify_email(request.POST['email'], c1)
            return JsonResponse({"message": "Successfully registered please check your mail for api key", "status": 1})


def prediction(request):
    if request.method == "POST":
        data = request.POST.copy()
        print(data)
        try:
            c1 = Customer.objects.filter(key=request.POST['key'])[0]
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Invalid API Key", "status": -1})
        if c1.hit<=c1.max_hit:
            if request.FILES.get("image"):
                image = request.FILES["image"].read()
                output = predict(image)
                output['status'] = 1
                output['message'] = "API hitted successfully"
                c1.hit+=1

                c1.save()
                return JsonResponse(output)
            return JsonResponse({"message": "Please Upload an Image", "status": 0})
        return JsonResponse({"message": "Sorry your free API quota is over", "status": -2})


def verify_email(email, c1):
    key = uuid.uuid4()
    c1.key = key
    message = MIMEMultipart("alternative")
    message["Subject"] = "API Access Key"
    message["From"] = "teammember50@gmail.com"
    message["To"] = email
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           Thank You for registering for our services. <br>
           Your free trial api key is  <div style="background-color='blue'"><strong>""" + str(key) + """</strong></div><br>
           Go to <a href="www.deepiotics.com">Deepiotics</a> and try our services.
        </p>
      </body>
    </html>
    """
    msg = MIMEText(html, "html")
    message.attach(msg)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("teammember50@gmail.com", "amansohani13")
    s.sendmail("teammember50@gmail.com", email, message.as_string())
    s.quit()
    print("SENT")
    c1.save()
