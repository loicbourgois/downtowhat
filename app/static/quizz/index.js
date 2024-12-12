const request = async(path, body_json) => {
    return await request_url(path, body_json)
}


const request_url = async(url, body_json) => {
    const options = {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body_json)
    };
    const response = await fetch(url, options);
    return response;
}

const post = async(path, body_json) => {
    const r = await request(path, body_json) 
    const r2 = await r.json()
    return r2
}

const is_logged_in = async() => {
    const r = await post("is_logged_in")
    return r.is_logged_in
}


const get_anonymous_user_id = async(retried=false) => {
    const anonymous_user_id = localStorage.getItem("dtw.anonymous_user");
    if (anonymous_user_id && anonymous_user_id.length > 20 ) {
        return anonymous_user_id
    } else {
        localStorage.setItem("dtw.anonymous_user", (await post("get_new_anonymous_user_id")).value )
        if (retried === true) {
            return
        }
        return await get_anonymous_user_id(retried=true)
    }
}


document.answer = async (user_id, a, b, choice) => {
    const ack = await post("set_anonymous_answer", {
        user_id: user_id,
        a: a,
        b: b,
        choice: choice
    })
    location.reload()
}


document.reset_option = async (user_id, option_id) => {
    const ack = await post("reset_anonymous_option", {
        user_id: user_id,
        option_id: option_id,
    })
    location.reload()
}


document.set_other_user = (public_user_id) => {
    localStorage.setItem("dtw.other_user",  public_user_id)
    location.reload()
}


const go = async() => {
    if (is_logged_in() === true ) {
    } else {
        const auid = await get_anonymous_user_id()
        const question = await post("get_anonymous_question", {
            auid: auid
        })
        document.getElementById("options").innerHTML = `
            <button onclick="answer('${auid}', '${question.a}', '${question.b}', 'a')">${question.a_label}</button>
            <button onclick="answer('${auid}', '${question.a}', '${question.b}', 'b')">${question.b_label}</button>
        `
        const ranking = await post("get_anonymous_ranking", {
            user_id: auid
        })
        document.getElementById("username").innerHTML = ranking.username[0].username
        for (const x of ranking.rankings) {
            let circle = "🟢"
            const r = Math.ceil(parseFloat(x.win_ratio) * 100)
            if (r < 66) {
                circle = "🟡"
            }
            if (r < 33) {
                circle = "🔴"
            }
            document.getElementById("ranking").innerHTML += `
                <div >
                    <button class="small negative" onclick="reset_option('${auid}', '${x.option_id}')">reset</button>
                    <span>${circle}</span>
                    <span>${x.option_label}</span>
                </div>
            `
        }
        const matches = await post("get_anonymous_matches", {
            user_id: auid
        })
        for (const x of matches) {
            const s = Math.ceil(parseFloat(x.score) * 100)
            let pre_space = ""
            if (s < 100) {
                pre_space = " "
            }
            if (s < 10) {
                pre_space = "  "
            }
            document.getElementById("matches").innerHTML += `
                <div >
                    <span class="percent_match">${pre_space}${s}%</span>
                    <button class="small positive" onclick="set_other_user('${x.public_user_id}')">${x.username}</button>
                </div>
            `
        }
        const public_user_id = localStorage.getItem("dtw.other_user")
        if (public_user_id) {
            const ranking_2 = await post("get_anonymous_ranking_2", {
                public_user_id: public_user_id,
                user_id: auid,
            })
            if (ranking_2.username && ranking_2.username.length) {
                document.getElementById("username_2").innerHTML = ranking_2.username[0].username
            }
            if (ranking_2.username && ranking_2.score.length) {
                document.getElementById("score").innerHTML = Math.ceil(parseFloat(ranking_2.score[0].score) * 100) + "%"
            }
            for (const x of ranking_2.rankings) {
                let circle = "🟢"
                const r = Math.ceil(parseFloat(x.win_ratio) * 100)
                if (r < 66) {
                    circle = "🟡"
                }
                if (r < 33) {
                    circle = "🔴"
                }
                document.getElementById("ranking_2").innerHTML += `
                    <div>
                        <span>${circle}</span>
                        <span>${x.option_label}</span>
                    </div>
                `
            }
        }
    }
}


go()
