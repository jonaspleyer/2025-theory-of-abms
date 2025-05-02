use rayon::prelude::*;
use std::io::Write;

use nalgebra::{SimdPartialOrd, Vector2};
use rand::{Rng, SeedableRng};

// General Parameters
const INTERACTION_RANGE: f64 = 1.5;
const DT: f64 = 0.1;
const DX_MOVE: f64 = 0.4;
const DOMAIN_MAX: f64 = 30.0;

// Parameters for Prey
const DIVISION_TIME: f64 = 3.0;

// Parameters for Predator
const NUTRIENT_INCREASE: f64 = 0.17;
const NUTRIENT_DECREASE: f64 = 0.01;
const INITIAL_NUTRIENTS: f64 = 0.4;
const DEVOUR_CHANCE: f64 = 0.15;
const NUTRIENT_DIVISION_THRESHOLD: f64 = 1.0;

#[derive(Clone, Copy, Debug, PartialEq, PartialOrd)]
enum Species {
    Predator { nutrients: f64 },
    Prey { age: f64 },
}

use Species::*;

#[derive(Clone)]
struct Agent {
    species: Species,
    pos: nalgebra::Vector2<f64>,
    removal: bool,
}

impl Agent {
    fn divide(&mut self) -> Agent {
        match &mut self.species {
            Predator { nutrients } => *nutrients *= 0.5,
            Prey { age } => *age = 0.,
        }
        self.clone()
    }

    fn update(&mut self, dt: f64) {
        match &mut self.species {
            Prey { age } => *age += dt,
            Predator { nutrients } => *nutrients -= NUTRIENT_DECREASE,
        }
    }

    fn interact(a1: &mut Self, a2: &mut Self, rng: &mut rand_chacha::ChaCha8Rng) {
        match (&mut a1.species, &mut a2.species) {
            (Predator { nutrients }, Prey { age }) => {
                if rng.random_bool(DEVOUR_CHANCE) {
                    *age = 0.;
                    a2.removal = true;
                    *nutrients += NUTRIENT_INCREASE;
                }
            }
            (Prey { age }, Predator { nutrients }) => {
                if rng.random_bool(DEVOUR_CHANCE) {
                    *age = 0.;
                    a1.removal = true;
                    *nutrients += NUTRIENT_INCREASE;
                }
            }
            _ => (),
        }
    }

    fn update_position(&mut self, rng: &mut rand_chacha::ChaCha8Rng) {
        self.pos += Vector2::from([
            rng.random_range(-DX_MOVE..DX_MOVE),
            rng.random_range(-DX_MOVE..DX_MOVE),
        ]);
        self.pos.simd_clamp([0.; 2].into(), [DOMAIN_MAX; 2].into());
    }
}

fn run_main(agents: &mut Vec<Agent>, dt: f64, rng: &mut rand_chacha::ChaCha8Rng) {
    // Interactions
    let n_cells = agents.len();

    // Update Positions
    agents.iter_mut().for_each(|a| a.update_position(rng));

    for n in 0..n_cells {
        for m in n + 1..n_cells {
            let mut agents_mut = agents.iter_mut();

            let a1 = agents_mut.nth(n).unwrap();
            let a2 = agents_mut.nth(m - n - 1).unwrap();

            let p1 = a1.pos;
            let p2 = a2.pos;

            if (p1 - p2).norm() <= INTERACTION_RANGE {
                Agent::interact(a1, a2, rng);
            }
        }
    }

    // Remove Agents which are flagged
    agents.par_iter_mut().for_each(|a| {
        if let Predator { nutrients } = a.species {
            if nutrients <= 0.0 {
                a.removal = true;
            }
        }
    });
    agents.retain(|a| !a.removal);

    // Division
    let new_agents: Vec<_> = agents
        .iter_mut()
        .filter_map(|agent| {
            agent.update(dt);
            let var = match agent.species {
                Prey { age } => rng.random_bool((age - DIVISION_TIME).clamp(0., 1.)),
                Predator { nutrients } => nutrients >= NUTRIENT_DIVISION_THRESHOLD,
            };
            if var {
                let new_agent = agent.divide();
                Some(new_agent)
            } else {
                None
            }
        })
        .collect();
    agents.extend(new_agents);
}

pub fn main() {
    use Species::*;
    let mut rng = rand_chacha::ChaCha8Rng::seed_from_u64(0);

    let n_prey = 300;
    let n_pred = 30;
    let mut agents: Vec<_> = (0..n_prey)
        .map(|_| Agent {
            species: Prey { age: 0. },
            pos: [
                rng.random_range(0.0..DOMAIN_MAX),
                rng.random_range(0.0..DOMAIN_MAX),
            ]
            .into(),
            removal: false,
        })
        .collect();
    agents.extend((0..n_pred).map(|_| {
        Agent {
            species: Predator {
                nutrients: INITIAL_NUTRIENTS,
            },
            pos: [
                rng.random_range(0.0..DOMAIN_MAX),
                rng.random_range(0.0..DOMAIN_MAX),
            ]
            .into(),
            removal: false,
        }
    }));

    let mut saves = Vec::new();
    let n_iter = 3000;
    let mut pb = kdam::tqdm!(total = n_iter);
    let mut pb2 = kdam::tqdm!(total = 1000, position = 1);
    'main_loop: for i in 0..n_iter {
        run_main(&mut agents, DT, &mut rng);
        if i % 2 == 0 {
            let n_pred = agents
                .iter()
                .map(|a| match a.species {
                    Species::Predator { nutrients: _ } => 1,
                    _ => 0,
                })
                .sum::<i64>();
            let n_prey = agents.len() as i64 - n_pred;
            saves.push((n_pred, n_prey));
            pb2.set_description(format!("Predator: {n_pred:6} Prey: {n_prey:6}"));
            let ratio = (n_pred as f64 / (n_pred + n_prey) as f64 * 1000.) as usize;
            pb2.update_to(ratio).unwrap();

            if n_prey == 0 || n_pred == 0 {
                break 'main_loop;
            }
        }
        use kdam::BarExt;
        pb.update(1).unwrap();
    }

    let mut file = std::fs::File::create("data.csv").unwrap();
    for (n_pred, n_prey) in saves {
        file.write_all(format!("{n_prey},{n_pred}\n").as_bytes())
            .unwrap();
    }
}
