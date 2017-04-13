from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib

def sendEmail(LOG_SUBJ, LOG_FROM, YOUR_MAIL, LOG_PASS, LOG_MSG, LOG_TOSEND):
	msg = MIMEMultipart()
	msg['Subject'] = LOG_SUBJ
	msg['From'] = LOG_FROM
	msg['To'] = YOUR_MAIL
	msg.preamble = LOG_MSG
	# attach each file in LOG_TOSEND list
	for file in LOG_TOSEND:
		# attach text file
		if file[-4:] == '.txt':
			fp = open(file)
			attach = MIMEText(fp.read())
			fp.close()
		attach.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
		msg.attach(attach)

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(YOUR_MAIL, LOG_PASS)
	server.sendmail(LOG_FROM, YOUR_MAIL, msg.as_string())
	server.quit()