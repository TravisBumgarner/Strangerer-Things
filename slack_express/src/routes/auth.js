// Authorization codes may only be exchanged once and expire 10 minutes after issuance.
import axios from "axios"

import config from "../config"
// import { users } from "../db"

const generateBody = async ({ query }) => {
    const { code, state } = query
    let responseBody

    try {
        const axiosResponse = await axios({
            url: "https://slack.com/api/oauth.access",
            method: "get",
            params: {
                client_id: config.slack.client_id,
                client_secret: config.slack.client_secret,
                code
            }
        })
        if (axiosResponse.data.ok) {
            responseBody = "Success."

            const { access_token, scope, user_id, team_name, team_id } = axiosResponse.data
//            const user = await users.getById(user_id)
//            if (user.length) {
//                responseBody = "You're already registered! You can close this window."
//            } else {
//                const foo = await users.create({ user_id, team_id, team_name, access_token, scope })
//                responseBody = "All set! You can close this window."
//            }
        } else {
            responseBody = "An error has occured, please try again later."
        }
    } catch (error) {
        responseBody = "An error has occured, please try again later."
    }
    return responseBody
}

export default generateBody
