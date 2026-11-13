# Jev hands-on: sort a support inbox with typed questions

The code from the Runtime Explained short **"It doesn't chat. It decides."** (Let's Build It, EP 12).

> **Status of this code (13 November 2026)**
>
> - **Tested:** the questions, the thresholds and every result shown here and in the video. They come from a real run against `jev-1.13-free` on OpenCode.
> - **Not tested yet:** the connection lines at the top of `triage.py` (an OpenCode key read from `OPENCODE_API_KEY`). That run reached the free model without sending a key, which OpenCode's docs do not promise, so this file connects the documented way instead. Nobody has run that exact connection yet.
> - **If the first line fails for you:** check the key and the model name against [OpenCode's Jev docs](https://opencode.ai/docs/console/models/#jev), and please open an issue with the error. This note will be removed once the connection is confirmed.


**What Jev is.** A model from TypeSafe AI that does not write text. You give it some text (the *state*) and typed questions. It returns typed answers your code can use:

| Question type | You ask | You get back |
|---|---|---|
| `Choice` | Pick one of these options | The option, a confidence, and a probability for every option |
| `Score` | Rate it on this scale | A position on the scale, and a confidence |
| `Noul` | Is this statement true? | A probability from 0 to 1 |

`triage.py` sorts 12 support tickets for **Biscuit Labs, a made-up company**: which team, how angry, how urgent, and "send it to a human" when nothing fits.

## Set up

You need Python 3.10 or newer.

```bash
mkdir jev-inbox && cd jev-inbox
python3 -m venv .venv
source .venv/bin/activate
pip install typesafe-sdk
export OPENCODE_API_KEY="your-key"
# put tickets.txt and triage.py in this folder
python triage.py
```

**About access (what we saw on 13 November 2026):**

- Signing up at TypeSafe was immediate (one quiz question, no waitlist), but the account started at a $0.00 balance and the Playground would not run our own text until credits were added.
- OpenCode hosts `jev-1.13-free`, free for a limited time. That is the route this file uses. Their docs ask for an OpenCode Console API key.
- Using TypeSafe directly instead? Their quickstart connects with `TypeSafeClient(model="jev-latest")`, which reads `TYPESAFE_API_KEY`. Jev bills per input token there. We did not run this file that way.

## What you should see

```
billing            I was charged twice for my Potsy order t
technical          The pot keeps blinking orange even after
shipping   URGENT  My package was supposed to arrive last T
technical  URGENT  Your app has been crashing every time I 
billing            Can I get an invoice with my company's t
shipping           The box arrived crushed and the pot is c
human              Hi! No problem at all, I just wanted to 
human              Do you sell a version of Potsy for aquar
technical          It's not working.
billing    URGENT  I want my money back. This is the third 
technical          The app shows my plant as thirsty but I 
shipping           I ordered 3 pots last week and 4 more to
```

That is the output of our run (`jev-1.13-free`, about a quarter of a second per ticket). Yours may differ with another model version.

## The numbers behind it

| Ticket | Team (confidence) | Angry (0 to 2) | Urgent | Fits a team |
|---|---|---|---|---|
| I was charged twice for my Potsy order this mo… | billing (1.00) | 0.36 | 0.54 | 0.98 |
| The pot keeps blinking orange even after a ful… | technical (1.00) | 0.61 | 0.47 | 0.90 |
| My package was supposed to arrive last Tuesday… | shipping (1.00) | 0.99 | 0.75 | 0.98 |
| Your app has been crashing every time I open i… | technical (1.00) | 1.99 | 0.96 | 0.96 |
| Can I get an invoice with my company's tax num… | billing (1.00) | 0.00 | 0.26 | 0.95 |
| The box arrived crushed and the pot is cracked… | shipping (1.00) | 0.92 | 0.60 | 0.86 |
| Hi! No problem at all, I just wanted to say my… | technical (0.74) | 0.00 | 0.14 | 0.07 |
| Do you sell a version of Potsy for aquariums? … | technical (0.89) | 0.00 | 0.31 | 0.14 |
| It's not working.… | technical (1.00) | 0.88 | 0.52 | 0.62 |
| I want my money back. This is the third time I… | billing (1.00) | 1.74 | 0.80 | 0.75 |
| The app shows my plant as thirsty but I watere… | technical (1.00) | 0.01 | 0.14 | 0.63 |
| I ordered 3 pots last week and 4 more today. C… | shipping (1.00) | 0.00 | 0.53 | 0.98 |

Team, angry and urgent are from the three-question run. Fits is from the four-question run.

## Three things the video shows

1. **A Choice has to choose.** Without the `fits` question, "my cactus is named Kevin and he loves his new pot" went to `technical` with 0.74 confidence. The `fits` Noul scored it 0.07, so the rule sends it to a human. (Adding an `"other"` option also caught it in our run. TypeSafe's docs recommend the separate yes/no question.)
2. **0.5 is not a yes.** "It's not working." scored 0.52 on urgent. Near the middle, let a person decide.
3. **The model judges, your code acts.** The thresholds (0.3, 0.5, 0.7) live in your code, where you can change them.

## Honest notes

- The free model is available for a limited time, and it is version 1.13. The newest at the time of the video is 1.14.
- TypeSafe's docs say to keep arithmetic, counting and date logic in your own code. In our one test, a simple sum (3 + 4) was answered correctly, which proves very little.
- 12 tickets is a demo, not an evaluation. Test with your own messages before trusting it.
- If you tuned thresholds on one version, pin that version.

## Homework

1. Swap `tickets.txt` for ten of your own messages.
2. Change the three teams in `criteria` to yours, and update the `fits` question to match.
3. Run it, and look hardest at the ones it sent to the wrong place.

Docs: https://docs.typesafe.ai
