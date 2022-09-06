use crate::TwoStacks;
use std::fmt::Debug;

pub struct Queue<T: Debug + Default + Clone>{
    stack: TwoStacks::TwoStacks<T>,
    capacity: usize,
}

impl<T: Default + Clone + Debug> Queue<T>{
    pub fn new(n: usize) -> Queue<T>{
        Queue{
            stack: TwoStacks::TwoStacks::new(n+1),
            capacity: n,
        }
    }
    pub fn length(&self) -> Result<i32, &'static str>{
        self.stack.height(0)
    }
    pub fn enqueue(&mut self, item: T) -> Result<(), &'static str>{
        if self.length().expect("valid length") >= self.capacity as i32 { return Err("Not enough space in queue") }
        loop{
            match self.stack.pop(0){
                Ok(Some(c)) => self.stack.push(1, c).expect("error while transferring"),
                Ok(None) => break,
                Err(_) => break,
            };
        }
        self.stack.push(0, item).expect("Not enough space in queue!");
        loop{
            match self.stack.pop(1){
                Ok(Some(c)) => self.stack.push(0, c).expect("error while transferring"),
                Ok(None) => break,
                Err(_) => break,
            };
        }
        Ok(())
    }
    pub fn dequeue(&mut self) -> Result<Option<T>, &'static str>{
        self.stack.pop(0)
    }
}

impl<T: Debug + Default + Clone> std::fmt::Display for Queue<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", &self.stack.to_string())
    }
}

#[cfg(test)]
mod tests {
	use super::*;

    #[test]
    fn constructor_works() {
        let _q: Queue<i32> = Queue::new(10);
    }
    #[test]
    fn can_enqueue(){
        let mut q = Queue::new(10);
        q.enqueue("blah").unwrap();
        q.enqueue("blub").unwrap();
        println!("{}", q);
        assert_eq!(q.length().unwrap(), 2);
    }

    #[test]
    #[should_panic]
    fn max_size_works(){
        let mut q = Queue::new(5);
        for i in 0..10{
            q.enqueue(i).unwrap();
        }
    }

    #[test]
    fn can_dequeue(){
        let mut q = Queue::new(5);
        q.enqueue(5).unwrap();
        assert_eq!(q.dequeue().unwrap(), Some(5));
    }

    #[test]
    fn min_size_works(){
        let mut q = Queue::new(5);
        q.enqueue(5).unwrap();
        q.dequeue().unwrap();
        assert_eq!(q.dequeue().expect("no errors please!"), None);
    }

    #[test]
    fn display_works(){
        let mut q = Queue::new(2);
        q.enqueue("blah blah blah").unwrap();
        q.enqueue("lorem ipsum").unwrap();
        println!("{}", q);
    }
}