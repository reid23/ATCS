fn exact_change(target: u16, coins: &Vec<u8>) -> usize{
    let mut grid: u128 = 1<<target;
    for coin in coins{
        grid |= grid >> coin;
    }
    grid&1
}




fn main(){
    use std::time::Instant;
    let start = Instant::now();
    for i in 1..50{
        exact_change(700+i, &vec![1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25]);
    }
    println!("{}", start.elapsed().as_secs())
}