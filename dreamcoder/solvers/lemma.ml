open Printf
open Str
    
let ops = ["+"; "-"; "*"; "/"]
          
type 'a tree =
  (* Tree structure that stores equations in prefix tree form *)
  | Leaf
  | Node of 'a node 
and 'a node = {
  value: 'a;
  left: 'a tree;
  right: 'a tree
}

let getValue = function
  (* Returns value of a Tree since Tree.value raises error*)
  | Node x -> x.value
  | Leaf -> "Leaf"

let getLeft = function
  (* Returns left subtree of a Tree since Tree.left raises error*)
  | Node x -> x.left
  | Leaf -> Leaf

let getRight = function
  (* Returns right subtree of a Tree since Tree.right raises error*)
  | Node x -> x.right
  | Leaf -> Leaf

let rec getLength = function
  (* Returns number of nodes in tree (including root) *)
  | Leaf -> 0
  | Node x -> 1 + getLength x.left + getLength x.right 

let rec eq = function
  (* Compares two trees and checks if they are equal *)
  | Node x, Node y -> x.value=y.value && eq (x.left, y.left) && eq (x.right, y.right)
  | Leaf, Leaf-> true 
  | _ -> false;;

let rec dtrfy = function
  (* Converts tree to a string representation of form "(op left right)" *)
  | Leaf -> "" 
  | Node x -> "(" ^ x.value ^ (fun x -> if x<>"" then " "^x else x) (dtrfy x.left) ^ (fun x -> if x<>"" then " "^x else x) (dtrfy x.right) ^ ")"

let string_to_list s =
  (* Converts a string to a list of chars *)
  let rec exp i l =
    if i < 0 then l else exp (i - 1) (s.[i] :: l) in
  exp (String.length s - 1) []

let char_array_to_string s = 
  (* Converts a char array to a string *)
  let chars = Array.to_list s in 
    let buf = Buffer.create 16 in
      List.iter (Buffer.add_char buf) chars;
      Buffer.contents buf
 
let getOpenStack = fun charArr start ->
  (* For matching a "(" bracket to its corresponding ")" bracket, computes depth of stack for all characters in the array. First character reading left from our start position which has stack depth of 0 closes the bracket. *)
  let openStack = Array.make ((Array.length charArr)-start) 1 in 
    for i=1 to (Array.length openStack)-1 do
      let x = 
        if (Array.get charArr (start+i)) = '('
          then 1 
        else if (Array.get charArr (start+i)) = ')' 
          then -1
            else 0
      in
        Array.set openStack i ((Array.get openStack (i-1))+x) 
    done;
    openStack

let getClosedStack = fun charArr endS ->
  (* For matching a ")" bracket to its corresponding "(" bracket, computes depth of stack for all characters in the array. First character reading right from our endS position which has stack depth of 0 closes the bracket. *) 
  let closedStack = Array.make (endS+1) 1 in 
    for i= (endS-1) downto 0 do
      let x = 
        if (Array.get charArr (i)) = '('
          then -1 
        else if (Array.get charArr (i)) = ')' 
          then 1
            else 0
      in
        Array.set closedStack i ((Array.get closedStack (i+1))+x) 
    done;
    closedStack

let rec findZeroStart = fun intList i ->
  (* For a given openStack, finds first character reading left from our start position which has stack depth of 0 to close the "(" bracket.  *)
  if i >= Array.length intList then raise (Invalid_argument "Bracket not found.")
  else 
    if Array.get intList i =0 then i
    else findZeroStart intList (i+1)

let rec findZeroEnd = fun intList i ->
  (* For a given closedStack, finds first character reading right from our endS position which has stack depth of 0 to close the ")" bracket.  *)
  if i < 0 then raise (Invalid_argument "Bracket not found.")
  else 
    if Array.get intList i =0 then i
    else findZeroEnd intList (i-1)

let matchBracket = function 
  (* Returns index that closes the bracket in question, returns -1 if malformed input. *)
  | start, charArr, "(" -> findZeroStart (getOpenStack charArr start) start
  | endS, charArr, ")" -> findZeroEnd (getClosedStack charArr endS) endS
  | _ -> raise (Invalid_argument "Invalid input to matchBracket") 
  
let split_on_bracks = fun s -> split (regexp "(") s 
(* function for splitting string on "(" symbol to find if it contains only value and no left/right children *)

let rec trfy = fun s -> 
  (* Convert prefix equation string to a string tree *)
  if (List.length (split_on_bracks s)) >= 2
    then
      let charArr = string_to_list s |> Array.of_list in
      let subArr = Array.sub charArr 1 ((Array.length charArr)-2) in
      let rootVal = Array.sub subArr 0 1 in
      let arg1Start = 2 in
      let arg1End = matchBracket (arg1Start, subArr, "(") in
      let arg2End = (Array.length subArr)-1 in
      let arg2Start = matchBracket (arg2End, subArr, ")") in
      let leftArg = Array.sub subArr arg1Start (arg1End+1) in
      let rightArg = Array.sub subArr arg2Start (arg2End-arg2Start+1) in
      Node {value = char_array_to_string rootVal; 
            left = trfy (char_array_to_string leftArg);
            right = trfy (char_array_to_string rightArg);
      }
else
  if (List.length (split_on_bracks s)) = 1 
    then
      let charArr = string_to_list s |> Array.of_list in
      let subArr = Array.sub charArr 1 ((Array.length charArr)-2) in
      let rootVal = Array.sub subArr 0 (Array.length subArr) in 
      Node {value = char_array_to_string rootVal; 
            left = Leaf; 
            right = Leaf} 
  else
    if s = "()" || s=""
      then 
        Leaf
    else 
      raise (Invalid_argument ("Invalid input to trfy."^s))
;;

let permit_rotations = function
(* Checks if rotations are permissible or not*)
  | ("-", "-") -> (true, "-", "+")
  | ("-", "+") -> (true, "-", "-")
  | ("+", "+") -> (true, "+", "+")
  | ("+", "-") -> (true, "+", "-")
  | ("*", "*") -> (true, "*", "*")
  | ("*", "/") -> (true, "*", "/")
  | ("/", "/") -> (true, "/", "*")
  | ("/", "*") -> (true, "/", "/")
  | (a, b) -> (false, a, b)

let rrotatehelper = function
  (* Helper function to perform a right rotation on the tree *)
  | Node x -> 
    if (List.mem x.value ops) && (List.mem (getValue x.left) ops)
      then
        let (permitted, newOp1, newOp2) = permit_rotations ((getValue x.left), x.value) in
          if permitted = true then
            let originalRoot = newOp2 in
              let upperLeft = newOp1 in
                let upperRight = x.right in
                  let bottomLeft = getLeft x.left in
                  let bottomRight = getRight x.left in 
                    let rightSub = Node {value=originalRoot; left=bottomRight; right=upperRight} in
                      Node {value=upperLeft; left=bottomLeft; right=rightSub}
          else
            Node x
    else
      Node x
  | Leaf -> Leaf

let lrotatehelper = function
  (* Helper function to perform a left rotation on the tree *)
  | Node x -> 
    if (List.mem x.value ops) && (List.mem (getValue x.right) ops)
      then
      let (permitted, newOp1, newOp2) = permit_rotations (x.value, (getValue x.right)) in
      if permitted = true then
        let originalRoot = newOp1 in
          let upperLeft = x.left in
            let upperRight = newOp2 in
              let bottomLeft = getLeft x.right in
              let bottomRight = getRight x.right in 
                let leftSub = Node {value=originalRoot; left=upperLeft; right=bottomLeft} in
                  Node {value=upperRight; left=leftSub; right=bottomRight}
      else
        Node x
    else
      Node x
  | Leaf -> Leaf

let mathDomainDistHelper = function
  (* Helper function to perform a distribution operation on the tree *)
| Node x ->   
let leftLeft = (getLeft x.left) in 
  let leftRight = (getRight x.left) in 
    let rightLeft = (getLeft x.right) in 
      let rightRight = (getRight x.right) in 
        if ((x.value = "+" || x.value = "-")) 
          then 
          if ((getValue x.left) = "*" && (getValue x.right) = "*") || ((getValue x.left) = "/" && (getValue x.right) = "/")
            then
              if (eq (leftRight, rightRight))
                then
                  Node {value=(getValue x.left); 
                  left=Node{value=x.value; left=leftLeft; right=rightLeft};
                  right=leftRight}
              else
                if ((getValue x.left) = "*" && (getValue x.right) = "*") 
                  then 
                    if (eq (leftLeft, rightLeft))
                      then
                        Node {value=(getValue x.left); 
                        left=Node{value=x.value; left=leftRight; right=rightRight};
                        right=leftLeft}
                      else
                        Node x 
                else
                  Node x
          else
            Node x 
        else
          Node x
| Leaf -> Leaf

let mathDomainRevDistHelper = function
| Leaf -> Leaf
| Node x -> 
  let leftLeft = (getLeft x.left) in 
    let leftRight = (getRight x.left) in 
      let rightLeft = (getLeft x.right) in 
        let rightRight = (getRight x.right) in 
            if (x.value = "*" || x.value = "/")
              then 
                if (getValue x.left = "+" || getValue x.left = "-")
                  then 
                    Node {value=(getValue x.left); 
                          left = Node {value=x.value; left=leftLeft; right=x.right};
                          right= Node {value=x.value; left=leftRight; right=x.right}}
            else
              if (x.value = "*") 
                then if (getValue x.right = "+" || getValue x.right = "-")
                  then 
                    Node {value=(getValue x.right); 
                          left = Node {value=x.value; left=x.left; right=rightLeft};
                          right= Node {value=x.value; left=x.left; right=rightRight}}
          else 
            Node x
        else 
          Node x 
      else 
        Node x 

let rec genSub = fun s ->
  (* Generates all possible subtrees of a tree *)
  let eqTree = trfy s in 
    if eqTree!=Leaf then
      if (getLeft eqTree) = Leaf && (getRight eqTree) = Leaf
        then [s;]
      else
        [s;] @ genSub (dtrfy (getLeft eqTree)) @ genSub (dtrfy (getRight eqTree))
    else
      []

let rec reconstruct = fun i old newT ->
  (* Reconstructs a new tree by swapping in newT in the i-th indexed subtree of old. So if subtree "k" is at the i-th index of result of genSub(old), "k" in old gets replaced by newT. *)
  let subList = genSub old in
    let oldT = trfy old in
    if (i > List.length subList)
      then oldT
    else
      if i=0 then trfy newT
      else
        let leftLength = getLength (getLeft oldT) in
        if (i <= leftLength) then 
          Node {value = getValue oldT; 
                left = reconstruct (i-1) (dtrfy (getLeft oldT)) newT; 
                right = getRight oldT}
        else
          Node {value = getValue oldT; 
                left = getLeft oldT; 
                right = reconstruct (i-1-leftLength) (dtrfy (getRight oldT)) newT}

let treeop = fun s i operation ->
  (* Perform a tree operation on tree represented by string s. *)
  let allSubs = genSub s in 
    let selectedSub = List.nth allSubs i in
      let modifiedSub = operation (trfy selectedSub) in 
        reconstruct i s (dtrfy modifiedSub)

let op = fun s x opArg -> 
  (* Performs operation on x on both sides of tree. *)
  let allSubs = genSub s in 
    let selectedSub = List.nth allSubs x in
      let eqTree = trfy s in
        let valT = getValue eqTree in 
            let leftVal = getLeft eqTree in 
              let rightVal = getRight eqTree in
                if valT = "="
                  then 
                    dtrfy( Node {value=valT;
                        left= Node {value=opArg; left=leftVal; right= (trfy selectedSub)};
                        right= Node {value=opArg; left=rightVal; right= (trfy selectedSub)};
                        }
                        )
                else 
                  s

let reflHelper = function
  (* Swaps left and right subtrees in a tree for reflexive property*)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "=" )
      then Node {value=x.value; left = x.right; right = x.left}
    else
      Node x

let commHelper = function
  (* Swaps left and right subtrees in a tree for commutative property*)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "+" || x.value = "*")
      then Node {value=x.value; left = x.right; right = x.left}
    else
      Node x

let evalOp = function
  (* Determines operation z to perform on two confirmed integers x (z op) y *)
 | (x, y, "+") -> x+y
 | (x, y, "-") -> x-y
 | (x, y, "*") -> x*y
 | (x, y, "/") -> x/y 
 | _ -> raise (Invalid_argument "Invalid input to evalOp.")

let evalTree = fun x y z -> 
  (* Simplifies x (z op) y *)
    if (List.mem z ops) then
      let xVal = try Some (Option.get x) with Invalid_argument x-> None in 
        let yVal = try Some (Option.get y) with Invalid_argument y-> None in  
          if (xVal=None || yVal=None) 
            then None 
          else Option.some (evalOp ((Option.get x), (Option.get y), z))
    else 
      raise (Invalid_argument ("Invalid input to evalTree."^z))

let rec gcd a b =
  (* Computes Greatest Common Divisor of Two Integers*)
  if a<0 then 
    let c = -1*a in 
      if b = 0 then c
      else gcd b (c mod b)
  else
    if a = 0 then a
    else
      if b = 0 then a
      else gcd b (a mod b)

let div_evaluator var1 var2 leftVal rightVal rootval =
  (* Evaluates division expressions where both terms are constants *)
  if (var1 mod var2 = 0)
    then 
      Node {value = string_of_int (Option.get (evalTree leftVal rightVal rootval)); left=Leaf; right=Leaf} 
    else
      let currGCD = gcd var1 var2 in
        Node {value = rootval; 
              left=Node{value = string_of_int (var1 / currGCD); left=Leaf; right=Leaf}; 
              right= Node {value = string_of_int (var2 / currGCD); left=Leaf; right=Leaf}}

let evalHelper = function
(* evaluates a subtree if the leaves are numbers *)
  | Leaf -> Leaf
  | Node x ->
    let leftVal = int_of_string_opt (getValue x.left) in
      let rightVal = int_of_string_opt (getValue x.right) in
        if leftVal <> None && rightVal <> None
          then
            if x.value <> "/" then 
              Node {value = string_of_int (Option.get (evalTree leftVal rightVal x.value)); left=Leaf; right=Leaf}
            else
              let varA = Option.get leftVal in
              let varB = Option.get rightVal in
              if varA <> 0
                then
                if (varB<0)
                then 
                  let var1 = -1 * varA in
                  let var2 = -1 * varB in
                    div_evaluator var1 var2 leftVal rightVal x.value
                else
                  div_evaluator varA varB leftVal rightVal x.value
              else
                Node x
        else
          Node x

let addzeroHelper = function
  (* simplifies expression if 0 is being added to expression *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "+" && int_of_string_opt (getValue x.left) = Option.some 0) then
      x.right
    else
      if (x.value = "+" && int_of_string_opt (getValue x.right) = Option.some 0) then
        x.left
      else
        if (List.mem x.value ops) then
          Node {value="+"; left = Node{value=x.value; left = x.left; right = x.right}; right = trfy "(0)"}
        else
          Node x
  
let subzeroHelper = function
  (* simplifies expression if 0 is being subtracted from expression *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "-" && int_of_string_opt (getValue x.right) = Option.some 0) then
      x.left
    else
      if (List.mem x.value ops) then
        Node {value="-"; left = Node{value=x.value; left = x.left; right = x.right}; right = trfy "(0)"}
      else
        Node x

let multoneHelper = function
  (* simplifies expression if 1 is being multiplied to expression *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "*" && int_of_string_opt (getValue x.left) = Option.some 1) then
      x.right
    else
      if (x.value = "*" && int_of_string_opt (getValue x.right) = Option.some 1) then
        x.left
      else
        if (List.mem x.value ops) then
          Node {value="*"; left = Node{value=x.value; left = x.left; right = x.right}; right = trfy "(1)"}
        else
          Node x

let divoneHelper = function
  (* simplifies expression if 0 is being subtracted from expression *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "/" && int_of_string_opt (getValue x.right) = Option.some 1) then
      x.left
    else
      if (List.mem x.value ops) then
        Node {value="/"; left = Node{value=x.value; left = x.left; right = x.right}; right = trfy "(1)"}
      else
        Node x

let assocHelper = function
(* Performs associative operation on equation tree*)
| Leaf -> Leaf
| Node x ->
    if List.mem x.value ops && List.mem (getValue x.left) ops then
      if getValue x.left = "+" && (x.value = "+" || x.value = "-") then
        rrotatehelper (Node x)
      else if getValue x.left = "*" && (x.value = "*" || x.value = "/") then
        rrotatehelper (Node x)
      else Node x
    else if List.mem x.value ops && List.mem (getValue x.right) ops then
      if x.value = "+" && (getValue x.right = "+" || getValue x.right = "-") then
        lrotatehelper (Node x)
      else if x.value = "*" && (getValue x.right = "*" || getValue x.right = "/") then
        lrotatehelper (Node x)
      else Node x
    else Node x

let distHelper = function
(* Application of distributivity as specified in ConPoLe paper*)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "+" || x.value = "-") then
      mathDomainDistHelper (Node x)
    else 
      if (x.value = "*" || x.value = "/") then
        mathDomainRevDistHelper (Node x)
      else
        Node x

let subcommHelper = function
  (* Implements commutativity of subtraction operands*)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "-" && (getValue x.left) = "-") then
      Node {value=x.value; left = Node{value = (getValue x.left); left = (getLeft x.left); right = x.right}; right = (getRight x.left)}
    else
      Node x

let divselfHelper = function
  (* Divide by itself *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "/" && eq (x.left, x.right)) && not (eq (x.left, Leaf)) then
      trfy "(1)"
    else
      Node x

let subselfHelper = function
  (* Subtracts itself *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "-" && eq (x.left, x.right)) && not (eq (x.left, Leaf)) then
      trfy "(0)"
    else
      Node x

let subsubHelper = function
  (* Converts between + and - *)
  | Leaf -> Leaf
  | Node x ->
      let rightVal = int_of_string_opt (getValue x.right) in
        if (x.value = "-" && rightVal <> None) 
        then
          Node {value = "+"; left = x.left; right = Node {value = string_of_int (-1*(Option.get rightVal)); left = Leaf; right = Leaf}}
        else
          if (x.value = "-") 
            then
              Node {value = "+"; left = x.left; right = Node {value = "-"; left = trfy "(0)"; right = x.right}}
          else
            if (x.value = "+" && rightVal <> None) 
            then
              Node {value = "-"; left = x.left; right = Node {value = string_of_int (-1*(Option.get rightVal)); left = Leaf; right = Leaf}}
          else
            if (x.value = "+" && (getValue x.right) = "-" && (getRight x.right) = trfy "(0)")  
              then
                Node {value = "-"; left = x.left; right = (getRight x.right)}
            else
            Node x

let multzeroHelper = function
  (* Multiplies by 0 *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "*" && (int_of_string_opt (getValue x.left) = Option.some 0 || int_of_string_opt (getValue x.right) = Option.some 0)) then
      trfy "(0)"
    else
      Node x

let zerodivHelper = function
  (* Divides by 0 *)
  | Leaf -> Leaf
  | Node x -> 
    if (x.value = "/" && int_of_string_opt (getValue x.left) = Option.some 0) then
      trfy "(0)"
    else
      Node x

let _newConstGen = fun a b c -> ((a*b)+c)
  (* Generates new integers from existing primitives*)

let _add = fun s x ->
  (* Adds x on both sides of the equation *)
  op s x "+"

let _sub = fun s x ->
  (* Subtracts x on both sides of the equation *)
  op s x "-"

let _mult = fun s x ->
  (* Multiplies x on both sides of the equation*)
  op s x "*"

let _div = fun s x ->
  (* Divides by x on both sides of the equation *)
  op s x "/"

let _refl = fun s i ->
  (* Swaps left subtree with right subtree of equation stored in i-th indexed subtree of s. *)
  dtrfy (treeop s i reflHelper)

let _comm = fun s i ->
  (* Swaps left subtree with right subtree of equation stored in i-th indexed subtree of s. *)
  dtrfy (treeop s i commHelper)

let _assoc = fun s i ->
  (* Performs associative coupling/decoupling in i-th indexed subtree of s. *)
  dtrfy (treeop s i assocHelper)

let _dist = fun s i ->
  (* Implements distributive property in tree structure *)
  dtrfy (treeop s i distHelper)

let _subcomm = fun s i ->
  (* Implements distributive property in tree structure *)
  dtrfy (treeop s i subcommHelper)

let _eval = fun s i ->
  (* Evaluates the i-th indexed subtree of s *)
  dtrfy (treeop s i evalHelper)

let _addzero = fun s i ->
  (* When subtree involves addition of zero *)
  dtrfy (treeop s i addzeroHelper)

let _subzero = fun s i ->
  (* When subtree involves subtraction of zero *)
  dtrfy (treeop s i subzeroHelper)

let _multone = fun s i ->
  (* When subtree involves multiplication by one *)
  dtrfy (treeop s i multoneHelper)

let _divone = fun s i ->
  (* When subtree involves division by one *)
  dtrfy (treeop s i divoneHelper)

let _divself = fun s i ->
  (* When subtree involves division by the same term *)
  dtrfy (treeop s i divselfHelper)

let _subself = fun s i ->
  (* When division involves subtraction by the same term *)
  dtrfy (treeop s i subselfHelper)

let _subsub = fun s i ->
  (* Converts between + and - *)
  dtrfy (treeop s i subsubHelper)

let _multzero = fun s i ->
  (* When subtree involves multiplication by 0 *)
  dtrfy (treeop s i multzeroHelper)

let _zerodiv = fun s i ->
  (* When subtree involves division by 0 *)
  dtrfy (treeop s i zerodivHelper)


let _assoc_eval_add0Helper = function
|Leaf -> Leaf
|Node x ->
  let s1 = _assoc (dtrfy (Node x)) 0 in
  let eqTree = trfy s1 in
  if (not (eq ((getLeft eqTree), Leaf))) && (not (eq ((getRight eqTree), Leaf))) then
    let subListLength = (List.length (genSub (dtrfy (getLeft eqTree)))) + 1 in
    trfy(_addzero (_eval s1 subListLength) 0)
  else 
    Node x

let _assoc_eval_eval_add0Helper = function
|Leaf -> Leaf
|Node x ->
  if (not (eq ((Node x), Leaf))) && (not (eq (getLeft (Node x), Leaf))) && (not (eq (getRight (Node x), Leaf))) && (not (eq (getLeft (getLeft (Node x)), Leaf))) then
    let s1 = _assoc (dtrfy (Node x)) 1 in
    let eqTree = trfy s1 in
    let subListLength1 = (List.length (genSub (dtrfy (getLeft (getLeft eqTree)))))+2 in
    let s2 = _eval s1 subListLength1 in
    let subListLength2 = (List.length (genSub (dtrfy (getLeft (trfy s2)))) + 1) in
    let s3 = _eval s2 subListLength2 in
    trfy(_addzero s3 1)
  else
    Node x

let _dist_dist_eval_eval_eval_eval_multoneHelper = function
|Leaf -> Leaf
|Node x ->
  if (not (eq ((Node x), Leaf))) && (not (eq (getLeft (Node x), Leaf))) && (not (eq (getLeft (getLeft (Node x)), Leaf))) && (not (eq (getLeft (getLeft (getLeft (Node x))), Leaf))) && (not (eq (getRight (Node x), Leaf))) && (not (eq (getLeft (getRight (Node x)), Leaf))) then
    let s1 = _dist (dtrfy (Node x)) 2 in
    let s2 = _dist s1 1 in
    let subListLength1 = (List.length (genSub (dtrfy (getLeft (trfy s2)))))+2 in
    let s3 = _eval s2 subListLength1 in
    let subListLength2 = (List.length (genSub (dtrfy (getLeft (trfy s3)))) + 1) in
    let s4 = _eval s3 subListLength2 in
    let s5 = _eval s4 3 in
    let s6 = _eval s5 2 in
    trfy (_multone s6 1)
  else
    Node x

let _eval_evalHelper = function
|Leaf -> Leaf
|Node x ->
  if (not (eq ((Node x), Leaf))) && (not (eq (getLeft (Node x), Leaf))) then
    let s1 = _eval (dtrfy (Node x)) 1 in
    trfy(_eval s1 0)
  else
    Node x

let _assoc_eval_add0 = fun s i ->
  dtrfy (treeop s i _assoc_eval_add0Helper)
let _assoc_eval_eval_add0 = fun s i ->
  dtrfy (treeop s i _assoc_eval_eval_add0Helper)
let _dist_dist_eval_eval_eval_eval_multone = fun s i ->
  dtrfy (treeop s i _dist_dist_eval_eval_eval_eval_multoneHelper)
let _eval_eval = fun s i ->
  dtrfy (treeop s i _eval_evalHelper)

let _sub_eval_comm = fun s x ->
  let s1 = _sub s x in
  let s2 = _eval s1 (List.length (genSub (dtrfy (getLeft (trfy s1))))+1) in
  let eqTree = trfy s2 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) && (not (eq (getLeft (getLeft eqTree), Leaf))) then
    _comm s2 2
  else
    s

let _add_eval_comm_assoc_comm = fun s x ->
  let s1 = _add s x in
  let s2 = _eval s1 (List.length (genSub (dtrfy (getLeft (trfy s1))))+1) in
  let s3 = _comm s2 1 in
  let s4 = _assoc s3 1 in
  let eqTree = trfy s4 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) && (not (eq (getLeft (getLeft eqTree), Leaf))) then
    _comm s4 2
  else
    s

let _sub_eval_comm_assoc_eval_add0 = fun s x ->
  let s1 = _sub_eval_comm s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) then
    _assoc_eval_add0 s1 1
  else
    s

let _add_eval_comm_assoc_comm_assoc_eval_add0 = fun s x ->
  let s1 = _add_eval_comm_assoc_comm s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) then
    _assoc_eval_add0 s1 1
  else
    s

let _sub_assoc_eval_eval_add0 = fun s x ->
  let s1 = _sub s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) && (not (eq ((getLeft (getLeft eqTree)), Leaf))) then
    _assoc_eval_eval_add0 s1 0
  else
    s

let _sub_assoc_eval_eval_add0_multone = fun s x ->
  let s1 = _sub_assoc_eval_eval_add0 s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) then
    _multone s1 1
  else
    s

let _sub_subsub_comm_assoc_eval_eval_add0_multone = fun s x ->
  let s1 = _sub s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) && (not (eq ((getLeft (getLeft eqTree)), Leaf))) then
    let s2 = _subsub s1 2 in
    let s3 = _comm s2 2 in
    let s4 = _assoc_eval_eval_add0 s3 0 in
    _multone s4 1
  else
    s

let _div_eval_comm_assoc_eval_multone = fun s x ->
  let s1 = _div s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) then
    let s2 = _eval s1 (List.length (genSub (dtrfy (getLeft eqTree)))+1) in
    let s3 = _comm s2 2 in
    let s4 = _assoc s3 1 in
    let s5 = _eval s4 (List.length (genSub (dtrfy (getLeft (getLeft (trfy s4)))))+2) in
    _multone s5 1
  else
    s

let _div_comm_assoc_eval = fun s x ->
  let s1 = _div s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) then
    let s2 = _comm s1 2 in
    let s3 = _assoc s2 1 in
    _eval s3 (List.length (genSub (dtrfy (getLeft (getLeft (trfy s3)))))+2)
  else
    s

let _div_comm_assoc_eval_eval_multone = fun s x ->
  let s1 = _div s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) && (not (eq ((getLeft (getLeft eqTree)), Leaf))) then
    let s2 = _comm s1 2 in
    let s3 = _assoc s2 1 in
    let s4 = _eval s3 (List.length (genSub (dtrfy (getLeft (trfy s3))))+1) in
    let s5 = _eval s4 (List.length (genSub (dtrfy (getLeft (getLeft (trfy s4)))))+2) in
    _multone s5 1
  else
    s

let _sub_dist_comm_assoc_subself_eval = fun s x ->
  let s1 = _sub s x in
  let eqTree = trfy s1 in
  if (not (eq (eqTree, Leaf))) && (not (eq (getLeft eqTree, Leaf))) && (not (eq (getLeft (getLeft eqTree), Leaf))) && (not (eq (getRight eqTree, Leaf))) && (not (eq (getLeft (getRight eqTree), Leaf))) && (not (eq (getRight (getRight eqTree), Leaf))) then
    let s2 = _dist s1 1 in
    let s3 = _comm s2 (List.length (genSub (dtrfy (getLeft (trfy s2))))+2) in
    let s4 = _assoc s3 (List.length (genSub (dtrfy (getLeft (trfy s3))))+1) in
    let s5 = _subself s4 (List.length (genSub (dtrfy (getLeft (trfy s4))))+2+(List.length (genSub (dtrfy (getRight (getLeft (trfy s4))))))) in
    _eval s5 2
  else
    s

(* Tests *)
(* 
;;

;;

printf "%s" (_refl (dtrfy (trfy "(= (-7) (- (3) (/ (-7) (x))))")) 0);;
printf "\n";;
printf "%s" (_subcomm "(= (-7) (- (- (3) (-7)) (x)))" 2);;
printf "\n";;
printf "%s" (_assoc "(= (-7) (+ (3) (- (-7) (x))))" 2);;
printf "\n";;
printf "%s" (_dist "(= (-7) (* (3) (- (-7) (x))))" 2);;
printf "\n";;

printf "%s"
  (_multzero (_mult (_subself (_sub "(= (-7) (- (3) (/ (-7) (x))))" 1) 1) 1) 4)
;;

printf "\n";;

printf "%s"
  (_zerodiv (_div (_subself (_sub "(= (-7) (- (3) (/ (-7) (x))))" 1) 1) 1) 4)
;;

printf "\n";;
printf "%s" (_subsub (_add "(= (-7) (- (3) (/ (-7) (x))))" 1) 1);;
printf "\n";;
printf "%s" (_comm (_mult "(= (-7) (- (3) (/ (-7) (x))))" 1) 4);;
printf "\n";;
printf "%s" (_divself (_div "(= (-7) (- (3) (/ (-7) (x))))" 1) 1);;
printf "\n";;
printf "%s" (_addzero "(= (-7) (+ (0) (/ (-7) (x))))" 2);;
printf "\n";;
printf "%s" (_subzero "(= (-7) (- (3) (0)))" 2);;
printf "\n";;
printf "%s" (_eval "(= (-7) (- (3) (0)))" 2)
printf "\n";;
printf "%s" (_multone "(= (-7) (* (x) (1)))" 2)
printf "\n";;
printf "%s" (_divone "(= (-7) (/ (x) (1)))" 2);;
printf "\n";;
*)

(*
Expected Test Results:
(= (- (3) (/ (-7) (x))) (-7))
(= (-7) (- (- (3) (x)) (-7)))
(= (-7) (- (+ (3) (-7)) (x)))
(= (-7) (- (* (3) (-7)) (* (3) (x))))
(= (* (0) (0)) (0))
(= (/ (0) (0)) (0))
(= (- (-7) (7)) (+ (- (3) (/ (-7) (x))) (-7)))
(= (* (-7) (-7)) (* (-7) (- (3) (/ (-7) (x)))))
(= (1) (/ (- (3) (/ (-7) (x))) (-7)))
(= (-7) (/ (-7) (x)))
(= (-7) (3))
(= (-7) (3))
(= (-7) (x))
(= (-7) (x)) 
*)*)*)*)*)*)

(*
printf "\n";;
printf "%s" (_eval (_multone (_eval (_dist "(= (+ (* (-1) (x)) (* (2) (x))) (+ (-3) (4)))" 1) 2) 1) 2);;
printf "\n";;
printf "%s" (_eval (_addzero (_eval (_assoc (_sub (_multone "(= (+ (* (1) (x)) (2)) (-3))" 2) 3) 1) 3) 1) 2);;
printf "\n";;
printf "%s" (_eval (_eval (_multone (_eval (_assoc (_comm (_div (_eval "(= (* (-1) (x)) (+ (2) (3)))" 2) 2) 2) 1) 3) 1) 3) 2);;
printf "\n";;
printf "%s" (_eval (_multone (_eval (_dist "(= (+ (* (-1) (x)) (* (2) (x))) (+ (-3) (4)))" 1) 2) 1) 2);;
printf "\n";;
printf "%s" (_eval (_multone (_eval (_dist "(= (+ (* (-1) (x)) (* (2) (x))) (- (-3) (4)))" 1) 2) 1) 2);;
printf "\n";;
printf "%s" (_eval (_addzero (_eval (_assoc (_subsub (_multone (_add "(= (- (* (1) (x)) (2)) (-3))" 5) 3) 2) 1) 3) 1) 2);;
printf "\n";;
printf "%s" (_eval (_divself (_assoc (_multone "(= (* (1) (x)) (/ (* (2) (x)) (x)))" 1) 2) 4) 2);;
printf "\n";;
*)

(*
Expected Test Results:
(= (x) (1))
(= (x) (-5))
(= (x) (-5))
(= (x) (1))
(= (x) (-7))
(= (x) (-1))
(= (x) (2))
*)

(* 
printf "%s" (_assoc_eval_add0 "(- (+ (x) (3)) (3))" 0);;
printf "\n";;
printf "%s" (_assoc_eval_eval_add0 "(= (- (+ (x) (3)) (3)) (+ (2) (3)))" 0);;
printf "\n";;
printf "%s" (_sub_eval_comm "(= (+ (3) (x)) (-4))" 2);;
printf "\n";;
printf "%s"
  (_dist_dist_eval_eval_eval_eval_multone
     "(= (- (+ (* (3) (x)) (* (3) (x))) (* (5) (x))) (+ (+ (3) (4)) (4)))" 0)
;;
printf "\n";;
printf "%s" (_add_eval_comm_assoc_comm "(= (- (x) (2)) (1))" 3);;
printf "\n";;
printf "%s" (_sub_eval_comm_assoc_eval_add0 "(= (+ (3) (x)) (-4))" 2);;
printf "\n";;
printf "%s"
  (_add_eval_comm_assoc_comm_assoc_eval_add0 "(= (- (* (8) (x)) (9)) (5))" 5)
;;
printf "\n";;
printf "%s" (_sub_assoc_eval_eval_add0 "(= (+ (x) (3)) (5))" 3);;
printf "\n";;
printf "%s" (_sub_assoc_eval_eval_add0_multone "(= (+ (* (1) (x)) (3)) (5))" 5)
;;
printf "\n";;
printf "%s"
  (_sub_subsub_comm_assoc_eval_eval_add0_multone "(= (- (3) (x)) (5))" 2)
;;
printf "\n";;
printf "%s" (_div_eval_comm_assoc_eval_multone "(= (* (8) (x)) (14))" 2);;
printf "\n";;
printf "%s" (_div_comm_assoc_eval "(= (* (3) (x)) (2))" 2);;
printf "\n";;
printf "%s" (_div_comm_assoc_eval_eval_multone "(= (* (3) (x)) (6))" 2);;
printf "\n";;
printf "%s"
  (_sub_dist_comm_assoc_subself_eval "(= (* (5) (x)) (+ (* (2) (x)) (4)))" 5)
;;
printf "\n";;
printf "%s" (_eval_eval "(+ (- (3) (0)) (-7))" 0) 
*)

(*
(x)
(= (x) (5))
(= (- (+ (x) (3)) (3)) (-7))
(= (x) (11))
(= (- (+ (x) (2)) (2)) (3))
(= (x) (-7))
(= (* (8) (x)) (14))
(= (x) (2))
(= (x) (2))
(= (* (- (0) (x)) (1)) (2))
(= (x) (/ (7) (4)))
(= (* (x) (1)) (/ (2) (3)))
(= (x) (2))
(= (* (3) (x)) (+ (4) (0)))
(-4)
*)*)*)*)*)