from flask import Flask, request, render_template
app = Flask(__name__)
import redis
rconn = redis.StrictRedis(host='50.17.215.201', port=6379, db=0, password="reallylongandhardtoguesspassword")
ps = rconn.pubsub()
ps.subscribe('CMDS')


from wtforms import Form, TextField, validators, HiddenField

class CaptchaForm(Form):
    text = TextField('solve the captcha:', [validators.Length(min=0, max=40)])
    cid = HiddenField()



@app.route("/", methods=['GET', 'POST'])
def solver():
        if request.method == 'POST':
                form = CaptchaForm(request.form)
                form.validate()
                rconn.publish(int(form.cid.data), form.text.data)
                return "pulled id: %s" % form.cid.data
        else:
            src = ""
            for m in ps.listen():
                if m.get('type') == 'message':
                    src = m['data']
                    break
            #src = "1233212:<a href=derp.com>HEY</a>"
            li = src.split('<')
            _id = li[0]
            img_src = "<" + li[1]
            form = CaptchaForm()
            form.cid.data = _id
            form_html = "<form action='' method=POST >"
            form_html += "Solve captcha:"+ str(form.text.__html__())
            form_html += str(form.cid.__html__())
            form_html += "<br><input type=submit value='  submit  '></input>"
            form_html += "</form>"
            html = "<html> %s <br> %s </html>" % (img_src, form_html)
            return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)


