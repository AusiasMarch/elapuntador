from datetime import datetime, timedelta

import jwt

from core import config

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_google_token(encoded_token):
    jwt.decode(
        encoded_token,
        key={
  "9cef5340642b157fa8a4f0d874fe7900362d82db": "-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIGrOfmAWA7cgwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0xOTEwMjcxNDQ5MzRaFw0xOTExMTMwMzA0MzRaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC1Rc0g3otklfmtrbcYBbM9DbMl+PBDHO1q\n7psoNAf96GEnkIIEOkFwjId5sblYI4g383++plSh5i+pcpV+mZQhbg7+sWcqA/sr\n4xqXhUGo62YOzTP0crPvXbBToaZapCckEgPNOhOArkQ5FIxke1m9mvqO+vJljNmX\nLwGK3Zsxq5C3c5iUaVgCsMrYbLoTqiuojNjY7+ZFATS4Q3C7G1kcEijyOg7AQV8W\nM3qRRE2NPQqoV47bzP7QWiyKLJOurY2uOFd2JHG6zS3V+r/EnXgAc1o/MuPNhvpQ\nnQQkTnH/C5S8EMxuO9LVmWvwRXykIHN6oycfG+/D2WRYIrTMo66TAgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQCBdQNulvt4Z/agl2M6G4JPefl7kPzu\nMS1k5YxC/gBVidh02YNIY8yUDSR1V91Id9e1SQlEEMR5GMQB4PtKv1a186kWyCGL\nVB0tJJKXoZpGsku60u8lQBRhF6+FnhWPFETpwRiduZDf7DFHBbv0hWltapnRMxub\nttYuGFUoEurt9yYXn7XwhDUVAUPSuzOhdrjfq5Yvv8uNHTNd+cdW3Rmmou+6F3Yo\nCDEkXHnGH+90hZyr0T7/cMfEhSLj3vOeVAIP6Wpif2xLWuk6HQpE4LO2iK4zu0b5\nFEzNP6s7fXqmjyYbB1coQXIDPQyE7c2nuCSL2w7xSq9lvbFIgYB4MLOy\n-----END CERTIFICATE-----\n",
  "8a63fe71e53067524cbbc6a3a58463b3864c0787": "-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIOgLatvPIOogwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0xOTEwMTkxNDQ5MzRaFw0xOTExMDUwMzA0MzRaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDJs8t86KhuRio8l/ZL3xOQ/Rh2/PJKo9IA\n1rVHDxAS1PYjGrZ+7UMU6f3yt7WqNifkdA+Vboe+f//D0maUZ36YqD9cm+8RrzVO\nb60/21OuB+UCLONtMd9f36f00WUpr/VuUngcpifW+SGbCEI+a7Jd5vuwdkEie++O\nXiVpUHdVXCKCqCt5kEXrlqh0xxWQirMH7pXL9Yp5GoBH6w1wl/yx1I285LA89D+D\nDcxDfxKJ6bFVWR+efoBaJyG4Qj3tLbrgi7OA0kXlOKmlM+POMm/6rGKxEOoya9p6\nSLU8J7wJj0QpAnEFZk7LpaVt3LWCbM54uxcRUvkiwXIsZfpOrXaZAgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQAvsqHib9Zv36Z1u09/B1eUkrZovl9F\n8ZzzxkqNgrff9zBrtwstCPRPsz8LMaGWlDHcIqsLVe2nMbZp9ZGGCtZHoCKhiFnj\nOcNaixgGT8+wP6vn5SaNhZgu2AUNb9u6zc0IA59ggGeahSIkA17DqLqb7mIeLEj2\nTo7HTbEqjWZhl7zq01T/R7PQ5w/++InUL7HrXmwYczgJWCh6h5mU5jpYnuXRr+YI\nXEfZOaELe0HHxOfgtkY7P/f2Wb/ls0fbvYwqklxYN+jXjiopZevCoobWDlrGKZ1Z\nt114KpEaJ9RgL23tfePs32VV1NwVVnEtaWD2lijIO3AyIn+I7JHL7MDD\n-----END CERTIFICATE-----\n"
}
    )