# 💌 Бот с Анонимными Валентинками

![Python ver](https://img.shields.io/badge/pyhon-3.10-orange)
![aiogram](https://img.shields.io/badge/aiogram-3.13.1-blue)
![postgres](https://img.shields.io/badge/postgre-16-42a4ff)


Фановый `проект с использованием` разных уровней `транзакций`💻 на практике

## 💎 Суть проекта

1. В рамках идеи `Бот` выступает `Почтальон`ом📬 между `Отправителем` и `Получателем` сообщения.

2. Ради разнообразия проекта Было реализовано
    * Реферальная Система👥
    * Награды на приведённых пользователей🫣
    * Возможность узнать отправителя сообщения как бесплатно🆓, так и за скромную плату💸
    * Ведение активности пользователя по полученным и отправленным сообщениям📊
    * Возможность отправить 📷Фото/🎥Видео

## 🧩 Наполнение БД

> core > data > postgres.py 

В Проекте была использована одна таблица 📅 - `users`

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

## 👀 Отправка и Получение Анонимок

> core > app_essence > unknown_mes.py

#### 1. Пользователь переходит `по рефералке`👥 `или` отправляет её через команду `/anonim_message`
![case_1](https://sun9-64.userapi.com/impg/MHqc7JKBS49dJk4LWDAj7K-o1TXsAWN7mW0wjg/eyySrccSJjU.jpg?size=497x362&quality=95&sign=f804e8275aa0c912fcc06f325484b4f8&type=album)

#### 2. После этапа с текстовой частью сообщения Пользователь может `прикрепить` до 10 `Фото📷 или Видео🎥` 
![case_2](https://sun9-29.userapi.com/impg/_d7CeEhitkJaWzLhMDCmSskoiqme8Yqip1lwLQ/eEGkwElxfis.jpg?size=494x233&quality=95&sign=a44886d5d870c65f82f7dfb874818baf&type=album)

### 3. Псевдоним😶‍🌫️   
![case_3](https://sun9-48.userapi.com/impg/x0LYIoyNvYaiUks6YnM4wuutrYdBJFFQzigdzQ/LUhHUmVV-6M.jpg?size=491x172&quality=95&sign=cc84c6a06c7cd5e7391ddc306a74af56&type=album)

### 4. Подтверждение отправки сообщения |✅ ❌ ✏️|
![case_4](https://sun9-48.userapi.com/impg/lxqGlpJPO3B59gnbSzPNdVs0jzDTjlg6ppVoKA/QbgXLNxlCc0.jpg?size=478x622&quality=95&sign=dc7355d473d7d50e837d7a68daf38dc1&type=album)

### 5. Сторона Отправителя 📤 
![case_5](https://sun9-24.userapi.com/impg/5vLABPMc3whIgQdYiWIX4r0ZI7vdtQL9JOr23A/Hkd9ULOiW3o.jpg?size=495x223&quality=95&sign=b7a4c462602e9352cfd8fca1b921332c&type=album)

### 6. Сторона Получателя 📥
![case_6](https://sun9-32.userapi.com/impg/ockqUnUqXAHs1k7CJhRNRni0YvZ8MNJlkwQkTQ/xzpyluRJ4qU.jpg?size=499x455&quality=95&sign=83b9f174a7315b0553710ff2ea6b45fc&type=album)


## 🎩 Узнать Отправителя Сообщения

> core > app_essence > pay.py

#### После получения сообщения можно узнать его отправителя 🥸

![pay_1](https://sun9-26.userapi.com/impg/HdVZHghVhgxYC5bi2YkCh70xJI0TQ0vzYf4Y3w/bSjAO9spX9s.jpg?size=571x608&quality=95&sign=f7dbb5f5a67b58aeac5ef266f902a4f7&type=album)

#### Результат при разных способах оплаты идентичен ✅

![pay_2](https://sun9-56.userapi.com/impg/e8ItfuUl_0QAUpRR9FBgSPlUBcJlYCsL5WOdJw/z72LOmWJSAU.jpg?size=519x642&quality=95&sign=8cf069627a4818848fda8d1fa401693a&type=album)

## 👥 Реферальная Система

> core > app_essence > statistic_rewards.py 

#### «Узнать `1ого Отправителя` 👤 `за 3-х человек`👤👤👤, которые перешли по ссылке» - `/ref_rewards`

![f2p](https://sun9-15.userapi.com/impg/lXxy4T5hs5gjn7IUqwOiGTD3vQ-osKk6Klhd_A/YrZOZ-aEFMs.jpg?size=575x292&quality=95&sign=06c2163bbb948aec03d2f9dd031abebb&type=album)

## 📊 Статистика Пользователя

#### Вызывается по команде `/my_stats`

![stats](https://sun9-79.userapi.com/impg/AzcvKIDfTdYZx5yiRPOecCE3ZTqXSvzlpoxvMA/34g5EKsohd8.jpg?size=521x158&quality=95&sign=092f02caab5403f5425fcce94a86cf45&type=album)

# Спасибо За Прочтение✨😇