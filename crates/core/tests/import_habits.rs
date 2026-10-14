#[path = "support/shop_habits.rs"]
mod shop_habits;
use proptest::prelude::*;

#[test]
fn every_shop_habit_has_an_analytic_fixture() {
    for habit in 0..17 {
        shop_habits::checked_library(habit, 48, 36, -13, 21, 110013).unwrap();
    }
}

proptest! {
    #![proptest_config(shop_habits::config(64, concat!(env!("CARGO_MANIFEST_DIR"), "/tests/import_habits.proptest-regressions")))]
    #[test]
    fn random_shop_habits_preserve_analytic_parts(
        habit in 0u8..17, w in 20u32..80, h in 20u32..80,
        x in -100i32..100, y in -100i32..100, seed in any::<u64>(),
    ) {
        shop_habits::checked_library(habit,w,h,x,y,seed)?;
    }
}
