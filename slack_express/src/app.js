import axios from "axios"
import express from "express"
import bodyParser from "body-parser"
import AWS from  "aws-sdk"
import * as middleware from "./middleware"
import * as routes from "./routes"
import config from "./config"
import qs from 'querystring'

AWS.config.update({
  region: config.sqs.region,
  accessKeyId: config.sqs.access_key_id,
  secretAccessKey: config.sqs.secret_access_key
});

const SLACK_URL = 'https://slack.com/api';


const app = express()
const sqs = new AWS.SQS()


app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.use(middleware.validateSlackRequest)

app.post("/message", async (request, response, next) => {
    const responseBody = await routes.message(request.body)
    response.send(responseBody)
})

app.post("/message2", async (request, response, next) => {
    const { trigger_id } = request.body

    const dialog = {
        trigger_id,
        token: config.slack.oauth_token,
        dialog: JSON.stringify({
          callback_id: "will_said_something",
          "title": "What's up, Will?",
          "submit_label": "Request",
          "notify_on_cancel": true,
          "state": "Limo",
          "elements": [
              {
                  "type": "text",
                  "label": "Got a message for Joyce?",
                  "name": "message"
              },
              {
                "type": "text",
                "label": "Feeling stylish?",
                "name": "color"
            }
          ]
        })
      }
      axios.post(`${SLACK_URL}/dialog.open`, qs.stringify(dialog))
      .then((result) => {
        console.log(result.data)
        response.send('')
      }).catch((err) => {
        console.log(err)
        response.sendStatus(500);
      });
})

// app.get("/auth", async (request, response, next) => {
//     const responseBody = await routes.auth(request)
//     response.redirect("http://letspair.online/welcome")
// })

app.get("/ok", (request, response, next) => response.send("Service is running"))

app.get("/test-sqs", async (request, response, next) => {
    const params = {
        MessageBody: 'Hello',
        QueueUrl: config.sqs.url
    }
    sqs.sendMessage(params, (err, data) => { 
        if (err) {
            console.log(err.stack)
            response.json(err)
        } 
        response.send('ok')
    }) 
    // response.send('hello')
})



export default app
