# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    cat_app_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                box-sizing: border-box;
            }

            body, html {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: transparent;
            }

            #box {
                display: block;
                height: 100vh;
                width: 100vw;
                background-color: #f0f0f0;
                overflow: hidden;
                position: relative;
            }

            #box:hover {
                cursor: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' style='fill:black;font-size:100px;'><text y='90%'>🐭</text></svg>") 16 0, auto;
            }

            .cat * {
                text-align: center;
                margin-left: auto;
                margin-right: auto;
            }

            .cat, .ears, .eyes, .muzzle, .body, .paw, .tail, .tail-segment {
                position: relative;
            }

            .head, .body, .paw, .tail-segment {
                background-color: #000000;
            }

            .left {
                float: left;
            }

            .right {
                float: right;
            }

            .cat {
                position: absolute;
                top: calc(50% + 120px); /* Moved head/body down by 20px */
                left: 50%;
                transform: translate(-50%, -50%);
            }
            .head {
                width: 400px; 
                height: 360px;
                border-radius: 50%;
                z-index: 100;
                animation: head-bob 5s infinite ease-in-out;
            }

            @keyframes head-bob {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }

            /* Black Oval Body element */
            .body {
                width: 320px;          /* Proportionate width to the 400px head */
                height: 260px;         /* Gives it an elongated oval appearance */
                border-radius: 50%;    /* Turns the box into a clean oval geometry */
                top: -40px;            
                z-index: 10;           /* Lower than head (100) so it sits safely behind it */
                box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            }

            .ears {
                top: -80px;
                z-index: -100;
            }

            .ear {
                width: 0;
                height: 0;
                border-left: 100px solid transparent; 
                border-right: 100px solid transparent;
                border-bottom: 200px solid #000000;
            }

            .ear.left {
                transform: rotate(-20deg) translateX(-40px);
            }

            .ear.right {
                transform: rotate(20deg) translateX(40px);
            }

            .eyes {
                top: -72px;
                width: 70%;
            }

            .eye {
                width: 110px; 
                height: 110px;
                border-radius: 50%;
                background-color: #FFD700;
                animation: eye-blink 5s infinite;
                text-align: center;
                position: relative;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .pupil {
                width: 32px; 
                height: 32px;
                background-color: #000000;
                border-radius: 50%;
                position: absolute;
                transition: transform 0.02s linear; 
            }

            @keyframes eye-blink {
                0%, 100% { transform: scaleY(1); }
                18%, 22% { transform: scaleY(1); }
                20% { transform: scaleY(0); }
            }

            .muzzle {
                top: 220px;
            }

            .nose {
                width: 60px;               
                height: 36px;              
                background-color: pink; 
                border-radius: 45% 45% 55% 55% / 40% 40% 70% 70%;
                border-left: none;
                border-right: none;
                border-top: none;
            }
        </style>
    </head>
    <body>
        <div id="box">
            <div class="cat">
                <div class="head">
                    <div class="ears">
                        <div class="ear left"></div>
                        <div class="ear right"></div>
                    </div>
                    <div class="eyes">
                        <div class="eye left">
                            <div class="pupil"></div>
                        </div>
                        <div class="eye right">
                            <div class="pupil"></div>
                        </div>
                    </div>
                    <div class="muzzle">
                        <div class="nose"></div>
                    </div>
                </div>
                <div class="body"></div>
            </div>
        </div>

        <script>
            const pupils = document.querySelectorAll('.pupil');

            window.addEventListener('mousemove', (e) => {
                pupils.forEach((pupil) => {
                    const eye = pupil.parentElement;

                    const eyeRect = eye.getBoundingClientRect();
                    const eyeCenterX = eyeRect.left + eyeRect.width / 2;
                    const eyeCenterY = eyeRect.top + eyeRect.height / 2;

                    const angle = Math.atan2(e.clientY - eyeCenterY, e.clientX - eyeCenterX);
                    const maxDistance = 30; 

                    const distanceToMouse = Math.hypot(e.clientX - eyeCenterX, e.clientY - eyeCenterY);
                    const currentDistance = Math.min(maxDistance, distanceToMouse / 12);

                    const x = Math.cos(angle) * currentDistance;
                    const y = Math.sin(angle) * currentDistance;

                    pupil.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
                });
            });
        </script>
    </body>
    </html>
    """
    mo.Html(
        f"""
        <iframe 
            srcdoc="{cat_app_code.replace('"', '&quot;')}"
            sandbox="allow-scripts" 
            style="border: none; width: 100%; height: 500px; background: transparent; border-radius: 8px;"
        ></iframe>
        """
    )
    return


if __name__ == "__main__":
    app.run()
