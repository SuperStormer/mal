#![allow(dead_code)]

use std::rc::Rc;
use std::collections;
use std::fmt;
use super::printer::{escape_str,pr_list};
use super::env::{Env,env_new,env_bind};

#[deriving(Clone)]
pub enum MalType {
    Nil,
    True,
    False,
    Int(int),
    Strn(String),
    Sym(String),
    List(Vec<MalVal>),
    Vector(Vec<MalVal>),
    HashMap(collections::HashMap<String, MalVal>),
    Func(fn(Vec<MalVal>) -> MalRet),
    //Func(fn(&[MalVal]) -> MalRet),
    //Func(|Vec<MalVal>|:'a -> MalRet),
    MalFunc(MalFuncData),
}

pub type MalVal = Rc<MalType>;

pub type MalRet = Result<MalVal,String>;

#[deriving(Clone)]
pub struct MalFuncData {
    pub eval:     fn(MalVal, Env) -> MalRet,
    pub exp:      MalVal,
    pub env:      Env,
    pub params:   MalVal,
    pub is_macro: bool,
}

impl MalType {
    pub fn pr_str(&self, print_readably: bool) -> String {
        let _r = print_readably;
        let mut res = String::new();
        match *self {
            Nil => res.push_str("nil"),
            True => res.push_str("true"),
            False => res.push_str("false"),
            Int(v) => res.push_str(v.to_string().as_slice()),
            Sym(ref v) => res.push_str((*v).as_slice()),
            Strn(ref v) => {
                if print_readably {
                    res.push_str(escape_str((*v).as_slice()).as_slice())
                } else {
                    res.push_str(v.as_slice())
                }
            },
            List(ref v) => {
                res = pr_list(v, _r, "(", ")", " ")
            },
            Vector(ref v) => {
                res = pr_list(v, _r, "[", "]", " ")
            },
            HashMap(ref v) => {
                let mut first = true;
                res.push_str("{");
                for (key, value) in v.iter() {
                    if first { first = false; } else { res.push_str(" "); }
                    res.push_str(key.as_slice());
                    res.push_str(" ");
                    res.push_str(value.pr_str(_r).as_slice());
                }
                res.push_str("}")
            },
            // TODO: better native function representation
            //Func(ref v) => {
            Func(_) => {
                res.push_str(format!("#<function ...>").as_slice())
            },
            MalFunc(ref mf) => {
                res.push_str(format!("(fn* {} {})", mf.params, mf.exp).as_slice())
            },
            /*

//            Atom(ref v) => v.fmt(f),
            */
            //_ => { res.push_str("#<unknown type>") },
        };
        res
    }

    pub fn apply(&self, args:Vec<MalVal>) -> MalRet {
        match *self {
            Func(f) => f(args),
            MalFunc(ref mf) => {
                let mfc = mf.clone();
                let alst = list(args);
                let new_env = env_new(Some(mfc.env.clone()));
                match env_bind(&new_env, mfc.params, alst) {
                    Ok(_) => (mfc.eval)(mfc.exp, new_env),
                    Err(e) => Err(e),
                }
            },
            _ => Err("attempt to call non-function".to_string()),
        }

    }
}

impl PartialEq for MalType {
    fn eq(&self, other: &MalType) -> bool {
        match (self, other) {
            (&Nil, &Nil) |
            (&True, &True) |
            (&False, &False) => true,
            (&Int(ref a), &Int(ref b)) => a == b,
            (&Strn(ref a), &Strn(ref b)) => a == b,
            (&Sym(ref a), &Sym(ref b)) => a == b,
            (&List(ref a), &List(ref b)) |
            (&Vector(ref a), &Vector(ref b)) => a == b,
            (&HashMap(ref a), &HashMap(ref b)) => a == b,
            // TODO: fix this
            (&Func(_), &Func(_)) => false,
            (&MalFunc(_), &MalFunc(_)) => false,
            _ => return false,
        } 
    }
}

impl fmt::Show for MalType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.pr_str(true))
    }
}


// Convenience constructor functions
pub fn _nil() -> MalVal { Rc::new(Nil) }
pub fn _true() -> MalVal { Rc::new(True) }
pub fn _false() -> MalVal { Rc::new(False) }
pub fn _int(i: int) -> MalVal { Rc::new(Int(i)) }

pub fn symbol(strn: &str) -> MalVal { Rc::new(Sym(strn.to_string())) }
pub fn strn(strn: &str) -> MalVal { Rc::new(Strn(strn.to_string())) }
pub fn string(strn: String) -> MalVal { Rc::new(Strn(strn)) }

pub fn list(lst: Vec<MalVal>) -> MalVal { Rc::new(List(lst)) }

pub fn func(f: fn(Vec<MalVal>) -> MalRet ) -> MalVal {
    Rc::new(Func(f))
}
pub fn malfunc(eval: fn(MalVal, Env) -> MalRet,
               exp: MalVal, env: Env, params: MalVal) -> MalVal {
    Rc::new(MalFunc(MalFuncData{eval: eval, exp: exp, env: env,
                                params: params, is_macro: false}))
}
pub fn malfuncd(mfd: MalFuncData) -> MalVal {
    Rc::new(MalFunc(mfd))
}