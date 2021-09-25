const btnModals = [...document.getElementsByClassName('modal-button')];
const modalBody = document.getElementById('modal-body-confirm');
const btnForPk = document.getElementById('start-button')
const url = window.location.href
//console.log(url)

btnModals.forEach(btnModal => btnModal.addEventListener('click', () =>{
    //console.log(btnModal)
    const pk = btnModal.getAttribute('data-pk');
    const name = btnModal.getAttribute('data-name');
    const topic = btnModal.getAttribute('data-topic');
    const questions = btnModal.getAttribute('data-questions');
    const difficulty = btnModal.getAttribute('data-difficulty');
    const time = btnModal.getAttribute('data-time');
    const requiredPass = btnModal.getAttribute('data-pass');

    modalBody.innerHTML = `
    <div class = "h5 mb-3">Are you sure you want to begin ${name}?</div>
    <div class="text-muted">
        <ul>
            <li>Topic: ${topic}</li>
            <li>Number of Question: ${questions}</li>
            <li>Difficulty: ${difficulty}</li>
            <li>Duration: ${time}mins</li>
            <li>Required score to pass: ${requiredPass}%</li>
        </ul>
    </div>
    `

    btnForPk.addEventListener('click', () => {
        window.location.href = url + pk;
    });
}));
    