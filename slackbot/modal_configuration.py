CORRECT_TODAY_MESSAGE_SHORTCUT_CONFIRM_MODEL = {
    "private_metadata": "yeet",
    "type": "modal",
    "title": {
        "type": "plain_text",
        "text": "Today",
        "emoji": True
    },
    "submit": {
        "type": "plain_text",
        "text": "Correct!",
        "emoji": True
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": True
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "emoji": True,
                "text": "Are you sure that want to correct {}'s date?"
            }
        }
    ]
}

SEND_DATE_TO_CHANNEL_GLOBAL_SHORTCUT = {
    "private_metadata": "cats are better",
    "type": "modal",
    "title": {
        "type": "plain_text",
        "text": "Today",
        "emoji": True
    },
    "submit": {
        "type": "plain_text",
        "text": "Send!",
        "emoji": True
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": True
    },
    "blocks": [
        {
            "block_id": "my_block_id",
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": "Where would you like to post the date?"
            },
            "element": {
                "action_id": "my_action_id",
                "type": "conversations_select",
                "response_url_enabled": True,
                "default_to_current_conversation": True
            }
        }
    ]
}

TODAY_DISABLE_NOTIFICATIONS_APP_HOME = {  # TODO: Combine with the enroll homepage
    "type": "home",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Today's Date:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ""
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Settings:*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "Would you like to be notified of the date, everyday at 7:00 AM?"
                },
                {
                    "type": "mrkdwn",
                    "text": "_Pro Tip: You can also change these settings by using slash commands (`/today`) and shortcuts :zap:._"
                }
            ],
            "accessory": {
                "type": "radio_buttons",
                "initial_option": {
                    "text": {
                        "type": "plain_text",
                        "text": "Please don't"
                    },
                    "value": "disable_notifications",
                    "description": {
                        "type": "plain_text",
                        "text": "I don't believe in time."
                    }
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Please don't"
                        },
                        "value": "disable_notifications",
                        "description": {
                            "type": "plain_text",
                            "text": "I don't believe in time."
                        }
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Please do"
                        },
                        "value": "enroll_notifications",
                        "description": {
                            "type": "plain_text",
                            "text": "I'd like mommy to hold my hand and \npoint it to the date on a calendar."
                        }
                    }
                ]
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Today (this app) can tell you the date by using the slash command `/today`, the shortcuts (found in the :zap: button next to the message field, and finally can correct other people's delusions of today by using the shortcuts found in a message."
            }
        }
    ]
}

TODAY_ENROLL_NOTIFICATIONS_HOME = {
    "type": "home",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Today's Date:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "{}"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Settings:*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "Would you like to be notified of the date, everyday at 7:00 AM?"
                },
                {
                    "type": "mrkdwn",
                    "text": "_Pro Tip: You can also change these settings by using slash commands (`/today`) and shortcuts :zap:._"
                }
            ],
            "accessory": {
                "type": "radio_buttons",
                "initial_option": {
                    "text": {
                        "type": "plain_text",
                        "text": "Please do"
                    },
                    "value": "enroll_notifications",
                    "description": {
                        "type": "plain_text",
                        "text": "I'd like mommy to hold my hand and \npoint it to the date on a calendar."
                    }
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Please don't"
                        },
                        "value": "disable_notifications",
                        "description": {
                            "type": "plain_text",
                            "text": "I don't believe in time."
                        }
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Please do"
                        },
                        "value": "enroll_notifications",
                        "description": {
                            "type": "plain_text",
                            "text": "I'd like mommy to hold my hand and \npoint it to the date on a calendar."
                        }
                    }
                ]
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Your timezone is:* "
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Update Timezone",
                    "emoji": True
                },
                "value": "update_timezone_home"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "We use the timezone set on your Slack account."
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Today (this app) can tell you the date by using the slash command `/today`, the shortcuts (found in the :zap: button next to the message field, and finally can correct other people's delusions of today by using the shortcuts found in a message."
            }
        }
    ]
}