# from django.core.mail import send_mail
# from django.conf import settings

# def send_email_to_recipient(recipient_email: str, email_content: str, email_html_content: str, subject: str="no-reply@learningpost.ng"):
#     """
#     Sends an email to the specified recipient with the given content.
    
#     Args:
#         recipient_email (str): Email address of the recipient.
#         email_content (str): The HTML content format of the email.
#         subject (str, optional): Subject of the email. Defaults to "Notification".
    
#     Returns:
#         bool: True if email was sent successfully, False otherwise.
#     """
#     try:
#         send_mail(
#             subject=subject,
#             message=email_content,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[recipient_email],
#             fail_silently=False,
#             html_message=f"""
#             <!DOCTYPE html>
#             <html lang="en">
#             <head>
#                 <meta charset="UTF-8">
#                 <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                 <title>LearningPost.ng Email</title>
#             </head>
#             <body style="font-family: 'Inter', sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">
#                 <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
#                     <tr>
#                         <td align="center" style="padding: 20px 0;">
#                             <table width="100%" border="0" cellspacing="0" cellpadding="0" style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
#                                 <!-- Header -->
#                                 <tr>
#                                     <td style="background-color: #6082b640; padding: 20px; text-align: center; border-top-left-radius: 8px; border-top-right-radius: 8px; display: grid; place-items: center;">
#                                         <!-- Placeholder for logo. Replace with your actual logo URL -->
#                                         <img src="https://api.learningpost.ng/static/assets/images/logo_black.webp" alt="" style="border: 0; height: 60px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; display: block; border-radius: 4px;">
#                                     </td>
#                                 </tr>

#                                 <!-- Main Content -->
#                                 <tr>
#                                     <td style="padding: 30px; color: #333333; line-height: 1.6; font-size: 16px;">
#                                         {email_html_content}
#                                     </td>
#                                 </tr>

#                                 <!-- Call to Action Button -->
#                                 <tr>
#                                     <td style="text-align: center; padding: 20px 30px 30px;">
#                                         <a href="https://www.learningpost.ng" target="_blank" style="display: inline-block; background-color: #6082b6; color: #ffffff; padding: 15px 30px; border-radius: 5px; font-size: 16px; font-weight: 600; text-decoration: none;">Visit LearningPost.ng</a>
#                                     </td>
#                                 </tr>

#                                 <!-- Footer -->
#                                 <tr>
#                                     <td style="background-color: #f0f0f0; padding: 20px; text-align: center; font-size: 12px; color: #777777; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
#                                         <p style="margin: 0 0 10px;">&copy; 2025 LearningPost.ng. All rights reserved.</p>
#                                         <p style="margin: 0 0 10px;">
#                                             <a href="https://learningpost.ng/terms-and-conditions" style="color: #6082b6; text-decoration: none;">Terms and Conditions</a>
#                                             <span style="margin: 0 5px;">|</span>
#                                             <a href="https://learningpost.ng/privacy-policy" style="color: #6082b6; text-decoration: none;">Privacy Policy</a>
#                                         </p>
#                                         <div style="margin-top: 10px; display: flex; justify-content: center; gap: 10px;">
#                                             <!-- Social Media Icons (replace with actual links and icons if desired) -->
#                                             <a href="" style="padding: 5px 15px; background: #555555; color: #dadcdb; text-decoration: none;">
#                                                 <span>Call</span>
#                                             </a>
#                                             <a href="mailto:support@learningpost.ng" style="padding: 5px 15px; background: #555555; color: #dadcdb; text-decoration: none;">
#                                                 <span>Mail</span>
#                                             </a>
#                                         </div>
#                                     </td>
#                                 </tr>
#                             </table>
#                         </td>
#                     </tr>
#                 </table>
#             </body>
#             </html>

#             """
#         )
#         return True
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return False
