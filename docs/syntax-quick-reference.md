# HOI4 Syntax Quick Reference

This is a practical quick reference for the HOI4 scripting patterns most often needed when building mods with AI.

For full version-specific trigger and effect coverage, use the local HOI4 documentation files shipped with the game.

## Base syntax

```txt
key = value
key = { ... }
# comment
```

Common value shapes:

- `yes` / `no`
- numbers such as `1` or `0.25`
- identifiers such as `GER`, `mymod.1`, or `GER_industrial_push`

## Logic blocks

```txt
trigger = {
    tag = GER
    has_war = yes
    OR = {
        has_government = fascism
        has_government = neutrality
    }
    NOT = {
        has_completed_focus = GER_other_focus
    }
}
```

## Scope markers

Common scope references:

- `ROOT`
- `FROM`
- `PREV`
- `THIS`

Example:

```txt
FROM = { add_political_power = 50 }
PREV = { set_country_flag = my_flag }
```

## Focus template

```txt
focus_tree = {
    id = GER_custom_tree

    focus = {
        id = GER_industrial_push
        icon = GFX_goal_generic_construct_civ_factory
        x = 5
        y = 0
        cost = 10

        prerequisite = { focus = GER_previous_focus }
        mutually_exclusive = { focus = GER_other_path }

        available = {
            has_political_power > 50
        }

        bypass = {
            has_completed_focus = GER_skip_this_focus
        }

        completion_reward = {
            add_political_power = 100
            add_stability = 0.05
            country_event = { id = mymod.1 days = 1 }
        }

        ai_will_do = {
            factor = 1
        }
    }
}
```

Typical localisation:

- `GER_industrial_push`
- `GER_industrial_push_desc`

## Event template

```txt
add_namespace = mymod

country_event = {
    id = mymod.1
    title = mymod.1.t
    desc = mymod.1.d
    picture = GFX_report_event_generic

    is_triggered_only = yes

    trigger = {
        tag = GER
    }

    immediate = {
        set_country_flag = mymod_started
    }

    option = {
        name = mymod.1.a
        add_political_power = 50
    }
}
```

Typical localisation:

- `mymod.1.t`
- `mymod.1.d`
- `mymod.1.a`

## Decision template

```txt
political_decisions = {
    GER_special_category = {
        icon = generic_decision
        allowed = {
            original_tag = GER
        }

        GER_launch_campaign = {
            icon = generic_propaganda
            cost = 50
            days_remove = 30

            available = {
                has_political_power > 75
            }

            complete_effect = {
                add_war_support = 0.05
                country_event = mymod.2
            }
        }
    }
}
```

## Idea template

```txt
ideas = {
    country = {
        GER_new_spirit = {
            picture = idea_generic_political_reform
            modifier = {
                political_power_gain = 0.10
                stability_factor = 0.05
            }
        }
    }
}
```

Useful effects:

```txt
add_ideas = GER_new_spirit
remove_ideas = GER_new_spirit
add_timed_idea = {
    idea = GER_new_spirit
    days = 180
}
```

## Scripted helpers

Scripted effect:

```txt
GER_bonus_effect = {
    add_political_power = 50
    add_stability = 0.05
}
```

Call site:

```txt
GER_bonus_effect = yes
```

Scripted trigger:

```txt
GER_can_expand_trigger = {
    has_war = no
    num_of_civilian_factories > 20
}
```

Call site:

```txt
available = {
    GER_can_expand_trigger = yes
}
```

## On actions

```txt
on_actions = {
    on_startup = {
        effect = {
            GER = {
                country_event = { id = mymod.10 days = 5 }
            }
        }
    }
}
```

Use `on_daily` carefully because it can become expensive.

## Common triggers

```txt
tag = GER
original_tag = GER
has_war = yes
is_in_faction = no
has_government = fascism
has_completed_focus = GER_industrial_push
has_country_flag = my_flag
num_of_civilian_factories > 20
date > 1938.1.1
```

## Common effects

```txt
add_political_power = 100
add_stability = 0.05
add_war_support = 0.1
country_event = mymod.1
set_country_flag = my_flag
clr_country_flag = my_flag
complete_national_focus = GER_industrial_push
transfer_state = 64
```

## Localisation template

```yml
l_english:
 GER_industrial_push:0 "Industrial Push"
 GER_industrial_push_desc:0 "We must expand our industry."
 mymod.1.t:0 "A New Opportunity"
 mymod.1.d:0 "The cabinet proposes a bold reform."
 mymod.1.a:0 "Proceed."
 GER_new_spirit:0 "National Renewal"
```

## High-value pitfalls

- Always define an event namespace before event IDs.
- Focus, event, decision, and idea changes usually need localisation in the same pass.
- Many "it does nothing" bugs are actually scope bugs.
- Prefer reusable scripted helpers when logic appears more than once.
- Use the game log and CWTools before assuming your script structure is valid.
