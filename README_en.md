# 💌 Bot with Anonymous Valentines

![Python ver](https://img.shields.io/badge/pyhon-3.10-orange)
![aiogram](https://img.shields.io/badge/aiogram-3.13.1-blue)
![postgres](https://img.shields.io/badge/postgre-16-42a4ff)

A fan `project using` different levels of `transactions`💻 in practice

## 💎  Essence of the Project

1. As part of the idea, the `Bot` acts as a `Postman`📬 between the `Sender` and the `Recipient` of the message

2. For the sake of diversity, the project was implemented
    * Referral System👥
    * Rewards for listed users🫣
    * The opportunity to find out the sender of the message both for free🆓 and for a modest fee💸
    * Maintaining user activity based on received and sent messages📊
    * Ability to send 📷Photos/🎥Videos


## 🧩 Content DataBase

> core > data > postgres.py 

The project used one table 📅 - `users`

```sql
CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    tg_id bigint NOT NULL,
    f_name character varying(32) COLLATE pg_catalog."default",
    refer_hozain bigint,
    received_mes integer DEFAULT 0,
    sent_mes integer DEFAULT 0,
    refs_all_time integer DEFAULT 0,
    refs_rewards integer DEFAULT 0,
    free_deunknowns integer DEFAULT 0,
    CONSTRAINT "users _pkey" PRIMARY KEY (id),
    CONSTRAINT users_tg_id_key UNIQUE (tg_id)
)

```

## 👀 Sending and Receiving Anonymous Letters

> core > app_essence > unknown_mes.py

#### 1. The user `follows the Referral Link`👥 `or` sends it via the command `/anonim_message`
![case_1](https://sun9-64.userapi.com/impg/MHqc7JKBS49dJk4LWDAj7K-o1TXsAWN7mW0wjg/eyySrccSJjU.jpg?size=497x362&quality=95&sign=f804e8275aa0c912fcc06f325484b4f8&type=album)

#### 2. After the stage with the text part of the message, the User can `attach` up to 10 `Photos📷 or Videos🎥`
![case_2](https://sun9-29.userapi.com/impg/_d7CeEhitkJaWzLhMDCmSskoiqme8Yqip1lwLQ/eEGkwElxfis.jpg?size=494x233&quality=95&sign=a44886d5d870c65f82f7dfb874818baf&type=album)

### 3. Alias 😶‍🌫️   
![case_3](https://sun9-48.userapi.com/impg/x0LYIoyNvYaiUks6YnM4wuutrYdBJFFQzigdzQ/LUhHUmVV-6M.jpg?size=491x172&quality=95&sign=cc84c6a06c7cd5e7391ddc306a74af56&type=album)

### 4. Confirmation of Sending a Message |✅ ❌ ✏️|
![case_4](https://sun9-48.userapi.com/impg/lxqGlpJPO3B59gnbSzPNdVs0jzDTjlg6ppVoKA/QbgXLNxlCc0.jpg?size=478x622&quality=95&sign=dc7355d473d7d50e837d7a68daf38dc1&type=album)

### 5. Sender's Side 📤 
![case_5](https://sun9-24.userapi.com/impg/5vLABPMc3whIgQdYiWIX4r0ZI7vdtQL9JOr23A/Hkd9ULOiW3o.jpg?size=495x223&quality=95&sign=b7a4c462602e9352cfd8fca1b921332c&type=album)

### 6. Recipient's Side 📥
![case_6](https://sun9-32.userapi.com/impg/ockqUnUqXAHs1k7CJhRNRni0YvZ8MNJlkwQkTQ/xzpyluRJ4qU.jpg?size=499x455&quality=95&sign=83b9f174a7315b0553710ff2ea6b45fc&type=album)

## 🎩 Find Out The Sender Of The Message

> core > app_essence > pay.py

#### After receiving a message, you can find out its sender 🥸

![pay_1](https://sun9-26.userapi.com/impg/HdVZHghVhgxYC5bi2YkCh70xJI0TQ0vzYf4Y3w/bSjAO9spX9s.jpg?size=571x608&quality=95&sign=f7dbb5f5a67b58aeac5ef266f902a4f7&type=album)

#### The Result is identical for different payment methods ✅

![pay_2](https://sun9-56.userapi.com/impg/e8ItfuUl_0QAUpRR9FBgSPlUBcJlYCsL5WOdJw/z72LOmWJSAU.jpg?size=519x642&quality=95&sign=8cf069627a4818848fda8d1fa401693a&type=album)

## 👥 Referral System

> core > app_essence > statistic_rewards.py 

#### «Find out `1 Sender` 👤 for `3 People` 👤👤👤 who clicked on the link» - `/ref_rewards`

![f2p](https://sun9-15.userapi.com/impg/lXxy4T5hs5gjn7IUqwOiGTD3vQ-osKk6Klhd_A/YrZOZ-aEFMs.jpg?size=575x292&quality=95&sign=06c2163bbb948aec03d2f9dd031abebb&type=album)


## 📊 User Statistics

#### Called by command `/my_stats`

![stats](https://sun9-79.userapi.com/impg/AzcvKIDfTdYZx5yiRPOecCE3ZTqXSvzlpoxvMA/34g5EKsohd8.jpg?size=521x158&quality=95&sign=092f02caab5403f5425fcce94a86cf45&type=album)

# Thanks For Reading✨😇