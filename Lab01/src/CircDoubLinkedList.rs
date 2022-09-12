struct Node<T>{
    pred: Option<&Node<T>>,
    next: Option<&Node<T>>,
    val: T,
}
impl<T> Node<T>{
    fn new(val: T){
        Node{
            pred: None,
            next: None,
            val: val
        }
    }
    fn con(&mut self, pred: Option<&Node<T>>, next: Option<&Node<T>>){
        self.pred = match pred{
            Some(node) => node,
            None => self.pred,
        };
        self.next = match next{
            Some(node) => node,
            None => self.next,
        };
    }
}

struct CircDoubLinkedList<T>{
    head: Option<Node<T>>
}

impl<T> CircDoubLinkedList<T>{
    fn new(){
        CircDoubLinkedList{
            head: None
        }
    }
    fn insert(&mut self, val: T){
        if self.head == None{
            self.head = Node::new(val);
            self.head.con(Some(&self.head), Some(&self.head))
        } else {
            self.head.pred.con(None, Some(&Node::new(val)));
            self.head.con(self.head.pred.next, None);
            self.head.pred.con(Some(&self.head), None);

        }
    }

}