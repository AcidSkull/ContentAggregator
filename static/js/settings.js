let settings = document.getElementById('settings');

settings.addEventListener('click', () =>{
    let popup = document.getElementsByClassName('popup');
    popup[0].style.display = 'block';
    popup[1].style.display = 'block';
});

window.onclick = function(event){
    if (event.target == modal){
        let popup = document.getElementsByClassName('popup');
        popup[0].style.display = 'none';
        popup[1].style.display = 'none';
    }
}