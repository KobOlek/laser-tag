const gameZone = document.querySelector('.gameZone');
const enemyDiv = '<div class="enemyTarget" id="enemyTarget" onmouseover="killEnemies()"></div>';
let enemy = document.getElementById('enemyTarget');
const hoverSound = document.getElementById('hoverSound');
const scorePlace = document.getElementById('score');

let score = 0
scorePlace.textContent = 'Score:' + score;

function spawnEnemies(){
    if(!gameZone.contains(enemy)){
        gameZone.innerHTML += enemyDiv;
        enemy = document.getElementById('enemyTarget');
        topCoordinate = Math.floor(Math.random() * 100) + 1;
        leftCoordinate = Math.floor(Math.random() * 100) + 1;
        enemy.style.top = topCoordinate + "%";
        enemy.style.left = leftCoordinate + '%';
    };
};
spawnEnemies();

function killEnemies(){
    gameZone.innerHTML = '';
    spawnEnemies();
    hoverSound.play();
    score+=50;
    scorePlace.textContent = 'Score:' + score;
};