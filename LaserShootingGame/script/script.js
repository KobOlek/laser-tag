const gameZone = document.querySelector('.gameZone');
const enemyDiv = '<div class="enemyTarget" id="enemyTarget" onmouseover="killEnemies()"></div>';
let enemy = document.getElementById('enemyTarget');
const hoverSound = document.getElementById('hoverSound');
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
};