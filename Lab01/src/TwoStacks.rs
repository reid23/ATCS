use std::{fmt::Debug};

pub struct TwoStacks<T: Debug + Default + Clone>{
    len: usize,
    arr: Vec<Option<T>>,
    ptrs: [i32; 2],
}


impl<T: Debug + Default + Clone> TwoStacks<T>{
    pub fn new(n: usize) -> TwoStacks<T> {
        TwoStacks{
            len: n,
            arr: vec![None; n],
            ptrs: [0, n as i32 - 1],
        }
    }
    pub fn height(&self, stack_num: usize) -> Result<i32, &'static str> {
        match stack_num{
            0 => Ok(self.ptrs[0]),
            1 => Ok((self.len as i32 - 1) - self.ptrs[1]),
            _ => Err("Expected 0 or 1 in call to TwoStack.height"),
        }
    }
    pub fn push(&mut self, stack_num: usize, item: T) -> Result<(), &'static str>{
        if self.ptrs[0] == self.ptrs[1] { return Err("Stack Overflow during call to TwoStack.push"); }
        if !(stack_num == 0 || stack_num == 1) { return Err("Expected stack_num = 0 or 1 in call to TwoStack.push"); }

        self.arr[self.ptrs[stack_num] as usize] = Some(item);
        self.ptrs[stack_num] += [1, -1][stack_num];

        Ok(())

    }
    pub fn pop(&mut self, stack_num: usize) -> Result<Option<T>, &'static str>{
        if !(stack_num == 0 || stack_num == 1) { return Err("Expected stack_num = 0 or 1 in call to TwoStack.pop"); }

        if self.height(stack_num).unwrap() == 0 {
            return Ok(None); 
        }

        self.ptrs[stack_num] += [-1, 1][stack_num];
        Ok(self.arr[self.ptrs[stack_num] as usize].clone())
    }
}

impl<T: Debug + Clone + Default> std::fmt::Display for TwoStacks<T>{
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "Stack 1: {:?}\nStack 2: {:?}", self.arr[..(self.ptrs[0] as usize)].to_vec(), self.arr[((self.ptrs[1]+1) as usize)..].to_vec())
    }
}

#[cfg(test)]
mod tests {
	use super::*;

    #[test]
    fn can_init(){
        let _s: TwoStacks<i32> = TwoStacks::new(5);
    }

    #[test]
    fn can_add_to_both_stacks(){
        let mut s = TwoStacks::new(5);
        s.push(0, 5).unwrap();
        s.push(1, 5).unwrap();
        s.push(1, 6).unwrap();
        s.push(1, 7).unwrap(); //tests that we can push more than half of the space to one stack
    }

    #[test]
    fn can_pop(){
        let mut s = TwoStacks::new(5);
        s.push(0, 5).unwrap();
        s.push(1, 6).unwrap();
        s.push(1, 7).unwrap();
        assert_eq!(s.pop(0).unwrap(), Some(5));
        assert_eq!(s.pop(0).unwrap(), None);
    }

    #[test]
    fn height_works(){
        let mut s = TwoStacks::new(5);
        s.push(0, 5).unwrap();
        assert_eq!(s.height(0).unwrap(), 1);
        assert_eq!(s.height(1).unwrap(), 0);
        s.push(1, 1);
        assert_eq!(s.height(1).unwrap(), 1);
        let _ = s.pop(0).unwrap();
        assert_eq!(s.height(0).unwrap(), 0);
    }

    #[test]
    #[should_panic]
    fn overflow_panics(){
        let mut s = TwoStacks::new(3);
        s.push(0, 1).unwrap();
        s.push(1, 2).unwrap();
        s.push(1, 3).unwrap();
        s.push(1, 4).unwrap();
    }

}