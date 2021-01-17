// �ϐ��A�萔�̏�����
let xBall = Math.floor(Math.random() * 300) + 50;
let yBall = 50;
const diameter = 50;

let vxBall = 5;
let vyBall = 5;

let xPaddle;
let yPaddle;
const paddleWidth = 100;
const paddleHeight = 25;

let video;
let classifier;

let action = "neutral";

function setup() {
    createCanvas(640, 480);
    xPaddle = width / 2;
    yPaddle = height - 100;

    const featureExtractor = ml5.featureExtractor("MobileNet", modelLoaded);
    featureExtractor.numClasses = 3;

    video = createCapture(VIDEO);
    video.hide();

    classifier = featureExtractor.classification(video, videoReady);

    // �e��{�^���̒ǉ�
    neutralButton = createButton("neutral");
    neutralButton.mousePressed(function() {
        classifier.addImage("neutral");
        console.log("Added neutral image.");
    });

    leftButton = createButton("left");
    leftButton.mousePressed(function() {
        classifier.addImage("left");
        console.log("Added left image.");
    });

    rightButton = createButton("right");
    rightButton.mousePressed(function() {
        classifier.addImage("right");
        console.log("Added right image.");
    });

    trainButton = createButton("train");
    trainButton.mousePressed(function() {
        classifier.train((loss) => {
            if (loss == null) {
                console.log("Training is complete!!");
                classifier.classify(gotResults);
            } else {
                console.log(loss);
            }
        });
    });
}

function draw() {

    // �J�����̉�ʂ𔽓]
    push();
    translate(width, 0);
    scale(-1.0, 1.0);
    image(video, 0, 0, width, height);
    pop();

    // �{�[���̕`��
   fill(255, 0, 255);
    noStroke();
    ellipse(xBall, yBall, diameter, diameter);

    xBall += vxBall;
    yBall += vyBall;

    if (xBall < diameter / 2 || xBall > width - diameter / 2) {
        vxBall *= -1;
    }

    if (yBall < diameter / 2 || yBall > height - diameter / 2) {
        vyBall *= -1;
    }

    // �p�h���̕`��
    fill(0, 255, 255);
    noStroke();
    rect(xPaddle, yPaddle, paddleWidth, paddleHeight);
    xPaddle = constrain(xPaddle, 0, width - paddleWidth);

    if ((xBall > xPaddle && xBall < xPaddle + paddleWidth) && (yBall + (diameter / 2) >=yPaddle)) {
        vxBall *= -1;
        vyBall *= -1;
    }

    // �F�����ʂŃp�h���𑀍�
    if (action === "left") {
        xPaddle -= 5;
    } else if (action === "right") {
        xPaddle += 5;
    }
}

function keyPressed() {
    if (keyCode === LEFT_ARROW) {
        xPaddle -= 50;
    } else if (keyCode === RIGHT_ARROW) {
        xPaddle += 50;
    }
}

function modelLoaded() {
    console.log("Model Loaded!");
}

function videoReady() {
    console.log("The video is ready!");
}

function gotResults(err, results) {
    if (err) {
        console.error(err);
    } else {
        action = results;
        console.log(results);
        classifier.classify(gotResults);
    }
}