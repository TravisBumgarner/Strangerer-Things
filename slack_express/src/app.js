import axios from "axios"
import express from "express"
import bodyParser from "body-parser"
import AWS from  "aws-sdk"
import * as middleware from "./middleware"
import * as routes from "./routes"
import { sqsConfig } from "./config"

AWS.config.update({
  region: sqsConfig.region,
  accessKeyId: sqsConfig.access_key_id,
  secretAccessKey: sqsConfig.secret_access_key
});

const app = express()
const sqs = new AWS.SQS()


app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.use(middleware.validateSlackRequest)

app.post("/message", async (request, response, next) => {
    const responseBody = await routes.message(request.body)
    response.send(responseBody)
})

// app.get("/auth", async (request, response, next) => {
//     const responseBody = await routes.auth(request)
//     response.redirect("http://letspair.online/welcome")
// })

app.get("/ok", (request, response, next) => response.send("Service is running"))

app.get("/test-sqs", async (request, response, next) => {
    const params = {
        MessageBody: 'Hello',
        QueueUrl: sqsConfig.url
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
