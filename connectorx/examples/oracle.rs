use anyhow::Error;
use connectorx::prelude::*;
use std::env;

fn main() -> Result<(), Error> {
    let _ = env_logger::builder().is_test(true).try_init();
    let dburl = env::var("ORACLE_URL").unwrap();
    let source = OracleSource::new(&dburl, 1).unwrap();
    let mut dst = ArrowDestination::new();
    let dispatcher = Dispatcher::<_, _, OracleArrowTransport>::new(
        source,
        &mut dst,
        &["select * from lineitem where l_orderkey < 100000"],
    );

    dispatcher.run()?;

    Ok(())
}
