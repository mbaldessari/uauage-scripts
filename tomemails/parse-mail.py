import email
import os

def save_plain_text_attachments(email_file, output_dir):
    # Open the email file
    with open(email_file, 'r') as f:
        msg = email.message_from_file(f)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    counter = 0
    # Loop through the parts of the email
    for part in msg.walk():
        print(f"{counter} -> {part.get_content_type()}: {part.get_content_charset()} -> {part.get_filename()}")
        counter += 1
        #filename = f"temp-{counter}"
        if part.get_content_type() == 'message/rfc822':
            filename = part.get_filename()
        # Check if the part is an attachment and is in text/plain format
        if part.get_content_type() == 'text/plain':
            # Get the filename of the attachment
            if filename:
                # Create the full path to save the attachment
                newname = filename.replace(".eml", ".txt")
                file_path = os.path.join(output_dir, newname)
                # Save the attachment to the specified output directory
                charset = part.get_content_charset()
                if charset is None:
                    charset = "utf-8"
                with open(file_path, 'w') as f:
                    f.write(part.get_payload(decode=True).decode(charset))
                print(f'Saved: {file_path}')

email_file = "../tom-mails.txt"
output_dir = "/tmp/mails"
save_plain_text_attachments(email_file, output_dir)
