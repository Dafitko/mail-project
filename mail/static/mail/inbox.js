document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);
  document.querySelector('#emails-view').addEventListener('click', event => {
    const element = event.target.closest('.email-box');
    if (element) {
      load_email(element.id);
    }
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      const emails_container = document.createElement('div');
      emails_container.className = 'emails-list';

      emails.forEach(email => {
        const email_div = document.createElement('div');
        email_div.className = `email-box ${email.read ? 'read' : 'unread'}`;
        email_div.id = email.id;
        email_div.innerHTML = `
          <span class="email-sender">${email.sender}</span>
          <span class="email-subject">${email.subject}</span>
          <span class="email-timestamp">${email.timestamp}</span>
        `;
        emails_container.appendChild(email_div);
      });
      document.querySelector('#emails-view').appendChild(emails_container);
    });
}

function load_email(email_id) {
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      const email_div = document.createElement('div');
      email_div.className = 'email-detail';

      const active_mailbox = document.querySelector('#emails-view h3').innerText;

      email_div.innerHTML = `
        <div class="email-header">
          <h2>${email.subject}</h2>
          <div class="email-meta">
            <div><strong>From:</strong> ${email.sender}</div>
            <div><strong>To:</strong> ${email.recipients.join(', ')}</div>
            <div class="text-muted"><strong>Date:</strong> ${email.timestamp}</div>
          </div>
        </div>
        <hr>
        <div class="email-body-content">${email.body}</div>
        <hr>
        <button class="btn btn-outline-primary btn-sm" id="reply-btn">Reply</button>
        ${active_mailbox !== 'Sent' ? `<button class="btn btn-outline-secondary btn-sm ml-2" id="archive-btn">${email.archived ? 'Unarchive' : 'Archive'}</button>` : ''}
      `;

      document.querySelector('#email-view').innerHTML = "";
      document.querySelector('#email-view').appendChild(email_div);

      // Reply button event listener
      document.querySelector('#reply-btn').addEventListener('click', () => {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;

        let subject = email.subject;
        if (!subject.startsWith("Re: ")) {
          subject = `Re: ${subject}`;
        }
        document.querySelector('#compose-subject').value = subject;

        const composeBody = document.querySelector('#compose-body');
        composeBody.value = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
        composeBody.focus();
        composeBody.setSelectionRange(0, 0);
      });

      // Archive button event listener (only if not viewing Sent mailbox)
      if (active_mailbox !== 'Sent') {
        document.querySelector('#archive-btn').addEventListener('click', () => {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: !email.archived
            })
          })
            .then(() => {
              load_mailbox('inbox');
            });
        });
      }
    });

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });

  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
}

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log('Success:', result);
      load_mailbox('sent');
    })
    .catch(error => {
      console.error('Error:', error);
    });
}