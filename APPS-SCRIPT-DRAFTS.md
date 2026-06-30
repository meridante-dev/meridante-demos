# Gmail draft maker — inline mockup + attachment (one-time setup)

This makes the dashboard's **"Open in Gmail"** button create a real Gmail **draft** in
**meridante.pt@gmail.com** with:
- the approved email text,
- the website mockup **shown inline** in the body (clearly formatted preview section),
- the same mockup **attached** as `mockup.jpg`,
- a line in the body that mentions the attachment.

The team member just opens **Drafts**, reviews, and hits Send.

> ⚠️ This is the only way to get an attachment + inline image into Gmail automatically — a plain
> compose link can't carry files. Until this is deployed, the button still works but only links the
> mockup preview (no attachment).

---

## Steps (≈4 minutes, do it while logged in as **meridante.pt@gmail.com**)

1. Go to **https://script.google.com** → **New project**.
2. Delete the sample code, paste **all of `Code.gs`** below.
3. Click **Save** (disk icon). Name it `Meridante Draft Maker`.
4. **Deploy → New deployment** → gear icon → **Web app**.
   - **Description:** draft maker
   - **Execute as:** **Me (meridante.pt@gmail.com)**
   - **Who has access:** **Anyone**
   - **Deploy**.
5. First time it asks to **authorize** → choose the meridante.pt account → *Advanced → Go to project (unsafe)* → **Allow** (it needs Gmail + fetch permission).
6. Copy the **Web app URL** (ends in `/exec`).
7. Send me that URL — I'll paste it into the dashboard's `CONFIG.DRAFT_ENDPOINT` and push. Done.

(If you ever change the code, use **Deploy → Manage deployments → Edit → New version** so the same URL keeps working.)

---

## Code.gs

```javascript
function doPost(e) {
  try {
    var p = JSON.parse(e.postData.contents);
    var fr = (p.lang === 'fr');

    // fetch the mockup image from the public dashboard and use it inline + attached
    var blob = UrlFetchApp.fetch(p.image).getBlob().setName('mockup.jpg');

    var head = fr ? 'Aperçu de votre nouveau site' : 'Pré-visualização do seu novo site';
    var note = fr
      ? 'La maquette est jointe à cet e-mail (mockup.jpg) et présentée ci-dessous :'
      : 'A maqueta está em anexo a este e-mail (mockup.jpg) e apresentada em baixo:';

    var bodyHtml = (p.body || '')
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');

    var html =
      '<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#222;line-height:1.65">' +
        bodyHtml +
        '<div style="margin:28px 0 6px;border-top:1px solid #e4e4e4;padding-top:20px">' +
          '<div style="font:600 16px Georgia,serif;color:#0c1322;margin-bottom:4px">' + head + '</div>' +
          '<div style="font-size:13px;color:#666;margin-bottom:14px">' + note + '</div>' +
          '<img src="cid:mockup" style="display:block;width:100%;max-width:600px;border:1px solid #ddd;border-radius:8px"/>' +
          '<div style="font-size:12px;color:#999;margin-top:7px">📎 mockup.jpg</div>' +
        '</div>' +
      '</div>';

    // plain-text fallback (clients that don't render HTML) — also mentions the attachment
    var plain = (p.body || '') + '\n\n— ' + head + ' —\n' + note + '\n[' + (fr ? 'voir la pièce jointe mockup.jpg' : 'ver o anexo mockup.jpg') + ']';

    GmailApp.createDraft(p.to, p.subject, plain, {
      htmlBody: html,
      inlineImages: { mockup: blob },
      attachments: [blob],
      name: 'Meridante'
    });

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('Meridante Draft Maker is running.');
}
```

---

## How the team uses it
1. Pick your name in the top bar (Sajid / Lucas / João).
2. On a lead, click **✉ Open in Gmail** → a draft is created in meridante.pt@gmail.com and a Gmail
   **Drafts** tab opens.
3. The newest draft (top of the list) has the email + the mockup shown inline + `mockup.jpg` attached.
   Review and **Send**.
4. Flip the **Mark as sent** toggle on the card — it stamps your name + date for the team.
