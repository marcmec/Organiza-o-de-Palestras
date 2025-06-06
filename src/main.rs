use std::{
    cmp::Reverse,
    fs::read_to_string
};

const MORNING_START: u32 = 9 * 60;
const LUNCH_TIME: u32 = 12 * 60;
const AFTERNOON_START: u32 = 13 * 60;
const NETWORKING_TIME: u32 = 17 * 60;

#[derive(Clone)]
struct Talk {
    name: String,
    duration: u32,
}

struct Slot {
    name: String,
    capacity: u32, // Em minutos
    used: u32,
    talks: Vec<Talk>,
}

fn parse_talk(line: &str) -> Talk {
    let talk_tuple: (&str, &str) = line.rsplit_once(' ').expect("Erro ao dividir título e duração!");
    let duration: u32;
    if talk_tuple.1 == "lightning" {
        duration = 5;
    } else if talk_tuple.1.ends_with("min") {
        duration = talk_tuple.1.replace("min", "").parse::<u32>().expect("Falha ao tratar duração!");
    } else {
        panic!("Formato de palestra inválido: {}", line);
    };
    Talk {
        name: talk_tuple.0.to_string(),
        duration,
    }
}

fn main() {
    let mut talks: Vec<Talk> = read_to_string("proposals.txt")
                                .expect("Erro ao ler arquivo!")
                                .lines()
                                .map(|line| line.to_string())
                                .map(|line| parse_talk(&line))
                                .collect();

    talks.sort_by_key(|a| Reverse(a.duration));

    let mut slots = vec![
        Slot {
            name: "A_morn".to_string(),
            capacity: 180,
            used: 0,
            talks: Vec::new(),
        },
        Slot {
            name: "A_after".to_string(),
            capacity: 240,
            used: 0,
            talks: Vec::new(),
        },
        Slot {
            name: "B_morn".to_string(),
            capacity: 180,
            used: 0,
            talks: Vec::new(),
        },
        Slot {
            name: "B_after".to_string(),
            capacity: 240,
            used: 0,
            talks: Vec::new(),
        },
    ];

    for talk in &talks {
        let mut assigned = false;
        for slot in &mut slots {
            if slot.used + talk.duration <= slot.capacity {
                slot.talks.push(talk.clone());
                slot.used += talk.duration;
                assigned = true;
                break;
            }
        }
        if !assigned {
            panic!("Não foi possível alocar a palestra: {}", talk.name);
        }
    }

    for track in ["A", "B"].iter() {
        println!("Track {}:", track);
        let morn_name = format!("{}_morn", track);
        let morn_slot = slots.iter().find(|s| s.name == morn_name).expect("Slot not found");
        let mut current = MORNING_START;
        for talk in &morn_slot.talks {
            println!("{:02}:{:02} {} {}min", (current / 60) % 24, current % 60, talk.name, talk.duration);
            current += talk.duration;
        }
        println!("{:02}:{:02} Almoço", (LUNCH_TIME / 60) % 24, LUNCH_TIME % 60);
        let after_name = format!("{}_after", track);
        let after_slot = slots.iter().find(|s| s.name == after_name).expect("Slot not found");
        current = AFTERNOON_START;
        for talk in &after_slot.talks {
            println!("{:02}:{:02} {} {}min", (current / 60) % 24, current % 60, talk.name, talk.duration);
            current += talk.duration;
        }
        println!("{:02}:{:02} Evento de Networking", (NETWORKING_TIME / 60) % 24, NETWORKING_TIME % 60);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_talk_minutes() {
        let line = "Diminuindo tempo de execução de testes em aplicações Rails enterprise 60min";
        let talk = parse_talk(line);
        assert_eq!(talk.name, "Diminuindo tempo de execução de testes em aplicações Rails enterprise");
        assert_eq!(talk.duration, 60);
    }

    #[test]
    fn test_parse_talk_lightning() {
        let line = "Rails para usuários de Django lightning";
        let talk = parse_talk(line);
        assert_eq!(talk.name, "Rails para usuários de Django");
        assert_eq!(talk.duration, 5);
    }

    #[test]
    #[should_panic(expected = "Formato de palestra inválido")]
    fn test_parse_talk_invalid() {
        let line = "StRinG dE PaLeStRa InVáLiDa";
        parse_talk(line);
    }
}
