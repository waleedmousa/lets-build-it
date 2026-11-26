# An AI image generator from scratch (EP 15)

`draw.py` starts with 3,000 dots of pure random noise and turns them into a picture. It is 74 lines of Python and needs one library, numpy.

The AI never learns to draw. It learns one small thing: given a noisy dot, guess the noise that was added. Run that guess backwards, a little at a time, and a picture appears out of static. This idea is called a **diffusion model**, and it is the same loop used by image generators such as Stable Diffusion.

## Run it

```
pip install numpy
python draw.py
```

It trains for about 20 seconds, then draws its picture in the terminal:

```
turn 1000: error 0.413
turn 2000: error 0.397
turn 3000: error 0.395
turn 4000: error 0.391
turn 5000: error 0.391
turn 6000: error 0.392
            ############################            
             ################### ##### #  #         
        #### #                  #      # ##         
        ###                             # ###       
    ## #        ####            ###        ####     
    #####       ###             #####       ####    
    ####        ####            ####        ####    
    ###         ####           ######        ###    
    ####                         #          ####    
    ####      #                     #        ###    
    ####    #####                 ######   # ####   
    ####  #  ####        #       #  ### #   #####   
    ### #       #####################       #####   
     ####     # #####################    # ####     
        ####               #             ###        
        ###                    #      # ##          
             ########################## #           
             ###### ######## # #########            
```

That smiley was not copied. Every `#` is a place where the dots ended up after 50 rounds of removing noise. About three out of four dots (76%) land on the picture.

Your numbers should match ours. The picture can differ by a few characters on a different processor, because tiny rounding differences grow over 6,000 rounds of training.

## The five parts

1. **The picture.** A smiley typed out of `#` signs. Every `#` becomes a small cloud of dots. That is the whole training set: one picture.
2. **Noise.** 50 steps that take the clean picture to pure static, by mixing in a little more random noise each step. We add the noise ourselves, so we always know exactly what it was.
3. **The brain.** A small neural network. It sees one noisy dot and which step it is at, and guesses the noise that was added.
4. **Training.** A guessing game: add noise, let the brain guess it, compare with the real answer, nudge the brain. 6,000 rounds.
5. **Drawing.** Start from pure static. Ask the brain where the noise is, take a little of it away, add a tiny random jiggle, and repeat 50 times.

The picture shows up late. At step 40 of 50 it is still a mess; it snaps into focus in the last ten steps.

## Break it (both are in the video)

**1. Skip the practice.** Train for 100 rounds, not 6,000:

```python
for turn in range(1, 101):
```

You get a blob. Only 47% of the dots land on the picture.

**2. Delete the jiggle.** In the drawing loop, remove these two lines:

```python
    if step > 0:
        dots += np.sqrt(add[step]) * rng.normal(size=dots.shape)
```

You would expect a cleaner picture. You get this:

```
                                                    
                                                    
                                                    
                                                    
                                                    
                  #               #                 
                 ##               #                 
                 ##               #                 
                                                    
                                                    
              ###                   #               
               ##                  ###              
                 ###################                
                     ############                   
                                                    
                                                    
                                                    
                                                    
```

Two eyes and a mouth, and no head. Without the small random push at each step, every dot slides to the same few safe spots and the rest of the picture is never drawn. A little randomness keeps the picture whole.

## Your turn: draw your own picture

Change the `PICTURE` at the top of the file. Here is a heart:

```python
PICTURE = [
    "..##...##..",
    ".####.####.",
    "###########",
    "###########",
    ".#########.",
    "..#######..",
    "...#####...",
    "....###....",
    ".....#.....",
]
```

```
        ##########          # # ### #       
       # # ##  ###            ## ###        
      ## ### # ###         # ##### ###      
     ## ### ########  ################## #  
### ###### ## ########  ################ ## 
### ## ######## ######## ##### ############ 
### #  ##### ####### ############### ###### 
####### # ######   ### ##### #############  
   ##### ## ##### ###############  # ###    
     # #### ######################## ###    
        #### # ######################       
         ####################### #          
            ###################             
             ################  #            
                # # #### ## #               
                  #######                   
                  ########                  
                     # #                    
```

Rules for your own picture: every row must be the same length, use `#` for ink and `.` for empty, and keep lines at least one character thick. Try your initial. Thin details are the hardest part for this small brain.

More things to try:

- Train longer (change `6001`) and see whether more than 76% of the dots land.
- Change `STEPS = 50` to 10 or 200.
- Change `default_rng(0)` to another seed. With seeds 1 to 5 we got between 75% and 77%.

## How this compares to the real thing

Ours knows exactly one picture and draws with 3,000 dots. Stable Diffusion was trained on billions of images with captions, works on about a million pixels per image, and lets your text prompt steer each step. It also uses a much larger network and works on a compressed version of the image. The loop is the same: start from static, remove noise, repeat.

## What we tested before publishing

- `draw.py` was downloaded fresh from this repo and run. It printed exactly the output above.
- The same output came out on Python 3.10, 3.12, 3.13 and 3.14, with numpy 1.26, 2.0 and 2.5.
- Both "break it" edits and the heart were applied exactly as written and gave the results shown.
- Tested on Linux. Nothing in the code is system-specific, but we have not run it on Windows or macOS ourselves.
