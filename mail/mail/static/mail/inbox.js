document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  document.querySelector('#compose-send').addEventListener('click', (event) => {
    event.preventDefault();
    send(document.querySelector('#compose-recipients').value,
        document.querySelector('#compose-subject').value,
        document.querySelector('#compose-body').value)
  })

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        let newCard = document.createElement('div');
        newCard.className = 'card';
        if (email.read === false) {
          newCard.style = 'margin: 6px;';
        } else {
          newCard.style = 'margin: 6px; background-color: lightgray;';
        }

        let newCardBody = document.createElement('div');
        newCardBody.className = 'card-body';

        let newCardContent = document.createElement('p');
        newCardContent.className = 'card-text';
        if (mailbox.localeCompare('inbox') === 0 || mailbox.localeCompare('archive') === 0) {
          newCardContent.innerHTML = '<strong>' + email.sender + '</strong>: ' + email.subject;
        } else {
          newCardContent.innerHTML = '<strong>' + email.recipients + '</strong>: ' + email.subject;
        }

        let newCardDate = document.createElement('p');
        newCardDate.className = 'card-text';
        newCardDate.innerHTML = '<small class="text-muted">' + email.timestamp + '</small>';

        newCardBody.append(newCardContent);
        newCardBody.append(newCardDate);
        newCard.append(newCardBody);

        if (mailbox.localeCompare('sent') === 0) {
          newCard.addEventListener('click', () => load_email(email.id, false));
        } else {
          newCard.addEventListener('click', () => load_email(email.id, true));
        }

        document.querySelector('#emails-view').append(newCard);
        console.log(email.subject);
      })
  });

}


function load_email(email_id, can_archive) {
  console.log(`Email: ${email_id} clicked!`);
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  mark_as_read(email_id);

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {            
    document.querySelector('#email-view').innerHTML = `<p><strong>From:</strong> ${email.sender}</p><p><strong>To:</strong> ${email.recipients}</p><p><strong>Subject:</strong> ${email.subject}</p>`;
    let newCardDate = document.createElement('p');
    newCardDate.className = 'card-text';
    newCardDate.innerHTML = '<small class="text-muted">' + email.timestamp + '</small>';
    
    let newCard = document.createElement('div');
    newCard.className = 'email-body';
    newCard.innerHTML = email.body;

    if (can_archive === true) {
      let archiveButton = document.createElement('button');
      archiveButton.className = "btn btn-outline-danger";
      archiveButton.innerHTML = "Archive";
      archiveButton.setAttribute("data-bs-toggle", "button");
      archiveButton.type = "button";
      archiveButton.style = "margin-bottom: 5px;";
      if (email.archived === true) {
        archiveButton.innerHTML = "Archived";
        archiveButton.className = "btn btn-outline-danger active";
        archiveButton.setAttribute("aria-pressed", "true");
      }
      archiveButton.addEventListener('click', () => toggle_archive(email_id, email.archived));
      document.querySelector('#email-view').append(archiveButton);
    }

    let replyButton = document.createElement('button');
    replyButton.className = "btn btn-primary";
    replyButton.innerHTML = "Reply";
    replyButton.type = "button";
    replyButton.style = "margin: 5px;";
    replyButton.addEventListener('click', () => reply(email.sender, email.subject, email.timestamp, email.body));

    document.querySelector('#email-view').append(newCard);
    document.querySelector('#email-view').append(newCardDate);
    document.querySelector('#email-view').append(replyButton);
  });
}


// Send e-mail
function send(rec, sub, bod) {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: rec,
        subject: sub,
        body: bod
    })
  })
  .then(result => {
    console.log(result);
    if (result.status === 201) {
      load_mailbox('sent');
    } else {
      alert(result.error);
    }
  })
}


// Mark e-mail as Read
function mark_as_read(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}


// Archive/Unarchive Email
function toggle_archive(email_id, archived) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !archived
    })
  })
  location.reload();
}


// Reply to Email 
function reply(recipients, subject, timestamp, body) {
  compose_email();
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = 'Re: ' + subject;
  document.querySelector('#compose-body').value = 'On '+ timestamp + ' ' + recipients + ' wrote: ' + body;
}