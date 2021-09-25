const quizBox = document.getElementById('quiz-box');
const url = window.location.href;
const timeCount = document.getElementById('time-count')
//console.log(url)
//let data;

const activateTime = (time) => {
    //console.log(time)
   if(time.toString().length < 2){
       timeCount.innerHTML = `<b>0${time}:00</b>`
   }else{
       timeCount.innerHTML = `<b>${time}:00</b>`
   }

   let minutes = time - 1
   let seconds = 60
   let displaySeconds
   let displayMinutes

   const timer = setInterval(() =>{
    //console.log('Im counting')
    seconds --
    if(seconds < 0){
        seconds = 59
        minutes --
    }
    if(minutes.toString().length < 2){
        displayMinutes = '0' + minutes
    }else{
        displayMinutes = minutes
    }
    if(seconds.toString().length < 2){
        displaySeconds = '0' + seconds
    }else{
        displaySeconds = seconds 
    }
    if(minutes === 0 && seconds === 0){
        //console.log("time over")
        /*YOU CAN ALSO CLEAR TIME LIKE THIS */
        timeCount.innerHTML =  `<b>00:00</b>`
        setTimeout(() =>{
            clearInterval(timer)
            alert("Count down finish")
            sendData()
        }, 500)
        /*clearInterval(timer)
        alert("Count down finish")
        sendData()*/
    }

    timeCount.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
   }, 1000)
}

$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        //console.log(response);
        const data = response.data
        console.log(data)
        
        if(data.length === 0){
            quizBox.innerHTML = `<h1>Question not added yet</h1>`
        }else{
            data.forEach(el => {
                for(const [question, answers] of Object.entries(el)){
                    quizBox.innerHTML +=   `
                    <hr>
                    <div class="mb-3">
                    <b>${question}</b>
                    </div>
                    `
                    answers.forEach(answer => {
                        quizBox.innerHTML += `
                        <div>
                        <input type="radio"  class="ans" id="${question}-${answer}" name="${question}" value="${answer}" />
                        <label for="${question}"><b>${answer}</b></label>
                        </div>
                        `
                    })
                }
            });
        }
        //let i = 0;
        
        activateTime(response.time)
    },
    error: function(error){
        console.log(error);
    }
});

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName("csrfmiddlewaretoken")
const scoreResult = document.getElementById('score-result')




sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if(el.checked){
            data[el.name] = el.value
        }else{
            if(!data[el.name]){
                data[el.name] = null
            }
        }
    })
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            //console.log(response)
           console.log(response.results) 
           results = response.results
           quizForm.classList.add("not-visible")
           scoreResult.innerHTML = `${response.Passed ? 'Congratulation! ': 'Opps..:( '} Your result is ${response.score}%` 
           results.forEach(res => {
               const resDiv = document.createElement("div")
               for(const [question, resp] of Object.entries(res)){
                   resDiv.innerHTML = question
                   const cls = ['container', 'p-3', 'test-light', 'h3']
                   resDiv.classList.add(...cls)

                   if (resp == 'Not answered'){
                       resDiv.innerHTML += '- not answered'
                       resDiv.classList.add('bg-danger')
                   }else{
                       const answer = resp['answered']
                       const correct = resp['correct_answer']

                       if(answer == correct){
                           resDiv.classList.add('bg-success')
                           resDiv.innerHTML +=  ` answered: ${answer}`
                       }else{
                           resDiv.classList.add('bg-danger')
                           resDiv.innerHTML +=  ` | correct_answer: ${correct}`
                           resDiv.innerHTML +=  ` answered: ${answer}`
                       }
                   }
               }
               const body = document.getElementsByTagName('BODY')[0]
               scoreResult.append(resDiv)
           })
        },
        error: function(error){
            console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e => {
    e.preventDefault()
    sendData()
})