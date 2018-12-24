import axios from "axios"
import express from "express"
import bodyParser from "body-parser"
import AWS from  "aws-sdk"
import * as middleware from "./middleware"
import * as routes from "./routes"
import {message} from "./db"
import config from "./config"
import qs from 'querystring'

const ALLOWABLE_MESSAGE_LENGTH = 20

AWS.config.update({
  region: config.sqs.region,
  accessKeyId: config.sqs.accessKeyId,
  secretAccessKey: config.sqs.secretAccessKey
});

const SLACK_URL = 'https://slack.com/api';

const app = express()
const sqs = new AWS.SQS()


app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.use(middleware.validateSlackRequest)

app.post("/dialog", async (request, response, next) => {
    const { trigger_id } = request.body

    const dialog = {
        trigger_id,
        token: config.slack.oauth_token,
        dialog: JSON.stringify({
          callback_id: "will_said_something",
          "title": "What's up, Will?",
          "submit_label": "Mommmmm!",
          "notify_on_cancel": true,
          "state": "Limo",
          "elements": [
              {
                  "type": "text",
                  "label": "Got a message for Joyce?",
                  "name": "message"
              },
              {
                "type": "select",
                "label": "Feeling stylish?",
                "name": "colors",
                "options": [
                    {
                        label: "Christmas Colors",
                        value: "CHRISTMAS_THEME"
                    },
                    {
                        label: "PS Colors",
                        value: "PS_THEME"
                    },
                    {
                        label: "Random Colors",
                        value: "RANDOM_THEME"
                    },
                    {
                        label: "RGBY Colors",
                        value: "CHS_THEME"
                    }
                ]
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

app.post("/form_submission", async (request, response, next) => {
    const data = JSON.parse(request.body.payload)
    const {submission:{message: content, colors}, user:{id, name} } = data 
    // const recentUsers = await message.getRecentUsers()
    // if(recentUsers.includes(id)){
    //     return response.json({
    //         "errors": [
    //           {
    //             "name": "message",
    //             "error": "Slow down there cowboy, others are trying to escape the upside down."
    //           },
    //         ]
    //       })   
    // }

    if(content.length > ALLOWABLE_MESSAGE_LENGTH){
        return response.json({
            "errors": [
              {
                "name": "message",
                "error": "The Demogorgon ate you because your message was too long. Please pick a shorter message. (<20)"
              },
            ]
          })
    }
    const responseBody = await routes.message({ user_id: id, user_name: name, colors, content })  
    // Slack API doesn't seem to care about messages in the next line
    const sqs_message = {
        content,
        colors
    }
    const result = await queue_sqs(sqs_message)
    console.log('result', id)
    console.log('token', config.slack.oauth_token)
    axios.post(`${SLACK_URL}/chat.postMessage`, {
        token: config.slack.oauth_token,
        channel: id,
        text: `Good luck <@${id}>, I hope it's not too late.`
      })
      .then((result) => {
        console.log(result.data)
        response.send('')
      }).catch((err) => {
        console.log(err)
        response.sendStatus(500);
      });
})

app.get("/ok", (request, response, next) => {
    response.send("Service is running")
})

const queue_sqs = (message) => {
    const params = {
        MessageBody: JSON.stringify(message),
        QueueUrl: config.sqs.url
    }
    sqs.sendMessage(params, (error, data) => { 
        if (error) {
            console.log(error.stack)
            return false
        } 
        console.log(data)
        return true
    }) 
}

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
