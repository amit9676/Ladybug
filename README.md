# Ladybug
### Ladybug is an exciting 2D battle game where ladybugs engage in intense combat to emerge victorious.
###Take control of a ladybug and engage in fast-paced battles against opponents and various challenges.

## Project theme:
The project was made during my second semester of the 3rd year of computer science degree.
<br>
Its purpose, beyond providing an entertaining game to pass the time, is to show my software development skills
in python beyond the studied in the computer science degree.


### To play the game - you can download it from the attached zip on releases section.
### Alternatively, you can download it from here:
https://shorturl.at/jzFNW

## Gameplay
In Ladybug Showdown, you control a ladybug character with the goal of defeating other ladybug.<br>
Both of the Ladybug start with 10000 hitpoints. your goal is to hit the other ladybug until he has no hitpoints left,
before it does it to you.
### in order to achieve this purpose there are several tools in your disposal:
- **fire ball:** Basic most projectile, going straight forward until it hits the enemy or exceeding the board surface.<br>
upon impact the for ball will take 10 hitpoints from the hit ladybug.<br>it has unlimited ammunition.
- **flamethrower:** The flamethrower is highly powerful weapon that unleashes a stream of fire.<br>
It has wider spread, does continuous damage,<br>
however it has a limited range, and limited ammunition that must be collected with the matching disc.
- **rocket:** A guided projectile. it automatically being guided at the enemy taking 100 hitpoints.<br>
the ladybug simply has to launch the rocket at the approximate direction of its target, and the rocket will do the rest.<br>
like the flamethrower - it has limited ammunition that needs to be collected with the appropriate discs.
the rocket has a duration of 10 seconds, if it did not hit an enemy in thi time, it will automatically explode.
<br><br>
- **war wagon:** The game also has a support unit called the war wagon.<br>
the war wagon crosses the board in a linear manner, and shoots its target with a machine gun that fires fireball with
much greater fire rate and projectile speed, making it a formidable support unit that you want at your side, and don't
want to face against.<br>
In addition of its equipped machine gun, the war wagon will run over anything in its path - inflicting substantial damage.
regardless if its friend or foe.<br>
the war wagon can be collected with the appropriate disc.

###Game Discs
In order to obtain the valuable tools above - you need to reach game discs.
The discs appear randomly on the board for a few seconds.
You need to reach for them before your opponent does or before it disappears.<br>
Be advised: your opponents will also seek out the discs.

###How to play keys:
By default, these are the keys in which you can play the game:<br>
- up arrow to advance
- right and left key arrows to turn right or left, respectively.
- spacebar to shoot fireball.
- 'a' key to fire flamethrower.
- 's' key to launch a rocket.

these keys can be changed in settings any time for anything the player wants. after the change, the changes made will
be saved for further use.

## Development:
The game was developed using pygame, and contains many various classes and units that work together with OOP principles.
<br>
for further examination of the code feel free to take a look in the repository.

### All rights reserved to Amit Goffer.


