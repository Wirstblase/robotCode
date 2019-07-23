//
//  mainViewController.swift
//  RobotController2.0
//
//  Created by Macbook on 5/26/19.
//  Copyright © 2019 wapps. All rights reserved.
//

import UIKit

class mainViewController: UIViewController, UICollectionViewDelegate, UICollectionViewDataSource {
    
    @IBOutlet weak var collectionView: UICollectionView!
    
    @IBOutlet weak var optionSelectorView: UIView!
    
    @IBOutlet weak var allbtn: UIButton!
    @IBOutlet weak var option1View: UIView!
    @IBOutlet weak var option2View: UIView!
    @IBOutlet weak var option3View: UIView!
    
    @IBOutlet weak var greenview: UIView!
    @IBOutlet weak var blueview: UIView!
    @IBOutlet weak var redview: UIView!
    
    
    @IBOutlet weak var selector: UIVisualEffectView!
    
    func initializeoptionselector(){
        
        optionSelectorView.layer.cornerRadius = 16
        option1View.layer.cornerRadius=16
        option2View.layer.cornerRadius=16
        option3View.layer.cornerRadius=16
        selector.layer.cornerRadius = 16
        
        greenview.layer.opacity=0
        blueview.layer.opacity=0
        
        allbtn.layer.cornerRadius=16
        allbtn.layer.opacity=0.2
        
    }
    
    @IBAction func allbtnpress(_ sender: Any) {
        option = 4
        UIView.animate(withDuration: animDurat, animations: {
            self.allbtn.layer.opacity=1
            self.selector.alpha=0
            self.changetogray()
            })
    }
    
    func changetoblue(){
        if(redview.layer.opacity>0)
        {
            redview.layer.opacity=redview.layer.opacity-1
        }
        if(greenview.layer.opacity>0)
        {
            greenview.layer.opacity=greenview.layer.opacity-1
        }
        blueview.layer.opacity=blueview.layer.opacity+1
    }
    func changetogreen(){
        if(redview.layer.opacity>0)
        {
            redview.layer.opacity=redview.layer.opacity-1
        }
        if(blueview.layer.opacity>0)
        {
            blueview.layer.opacity=blueview.layer.opacity-1
        }
        greenview.layer.opacity=greenview.layer.opacity+1
    }
    func changetored(){
        if(blueview.layer.opacity>0)
        {
            blueview.layer.opacity=blueview.layer.opacity-1
        }
        if(greenview.layer.opacity>0)
        {
            greenview.layer.opacity=greenview.layer.opacity-1
        }
        redview.layer.opacity=redview.layer.opacity+1
        
    }
    func changetogray(){
        blueview.layer.opacity=0
        redview.layer.opacity=0
        greenview.layer.opacity=0
    }
    
    var option = 2 //1-wifi, 2-server, 3-bluetooth
    var animDurat = 0.3
    
    @IBAction func option1Select(_ sender: Any) {
        if(option==1)
        {}//do nothing
        else if(option==2)
        {
            UIView.animate(withDuration: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: (-16-32)/2, y: 0)
                self.selector.layer.cornerRadius = 0
            })
            UIView.animate(withDuration: animDurat/2, delay: animDurat/2, animations: {
                    self.selector.transform = CGAffineTransform(translationX: -16-32, y: 0)
                    self.selector.layer.cornerRadius = 16
                self.changetogreen()
                })
        }
        else if(option==3)
        {
            UIView.animate(withDuration: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: 0, y: 0)
                self.selector.layer.cornerRadius = 0
            })
            UIView.animate(withDuration: animDurat/2, delay: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: -16-32, y: 0)
                self.selector.layer.cornerRadius = 16
                self.changetogreen()
            })
        }
        
        option=1
    }
    
    @IBAction func option2Select(_ sender: Any) {
        if(option==1)
        {
            UIView.animate(withDuration: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: (-16-32)/2, y: 0)
                self.selector.layer.cornerRadius = 0
            })
            UIView.animate(withDuration: animDurat/2, delay: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: 0, y: 0)
                self.selector.layer.cornerRadius = 16
                self.changetored()
            })
        }
        else if(option==2)
        {}//do nothing
        else if(option==3)
        {
            UIView.animate(withDuration: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: (16+32)/2, y: 0)
                self.selector.layer.cornerRadius = 0
            })
            UIView.animate(withDuration: animDurat/2, delay: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: 0, y: 0)
                self.selector.layer.cornerRadius = 16
                self.changetored()
            })
        }
        option=2
    }
    
    @IBAction func option3Select(_ sender: Any) {
        if(option==1)
        {
            UIView.animate(withDuration: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: 0, y: 0)
                self.selector.layer.cornerRadius = 0
            })
            UIView.animate(withDuration: animDurat/2, delay: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: 16+32, y: 0)
                self.selector.layer.cornerRadius = 16
                self.changetoblue()
            })
        }
        else if(option==2)
        {
            UIView.animate(withDuration: animDurat/2, animations: {
            self.selector.transform = CGAffineTransform(translationX: (16+32)/2, y: 0)
            self.selector.layer.cornerRadius = 0
        })
            UIView.animate(withDuration: animDurat/2, delay: animDurat/2, animations: {
                self.selector.transform = CGAffineTransform(translationX: 16+32, y: 0)
                self.selector.layer.cornerRadius = 16
                self.changetoblue()
            })
            
            option=3
        }
            
        else if(option==3)
        {}//do nothing
    }
    
    let media = ["Type 1","Type 2","Type 3","Custom"]
    let imagearray = ["icontype1.jpg","icontype2.jpg","cat.jpg","cat.jpg"]
    let type1 = ["1"]
    let type2 = ["1"]
    let type3 = ["2"]

    override func viewDidLoad() {
        super.viewDidLoad()
        
        initializeoptionselector()
        
        collectionView.delegate = self
        collectionView.dataSource = self

    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return media.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "CustomViewCell", for: indexPath) as! CustomCollectionViewCell
        
        cell.label.text = media[indexPath.row]
        cell.icon.image = UIImage(named: imagearray[indexPath.row])
        cell.layer.cornerRadius=30
        
        return cell
    }
    
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        
        if(indexPath.row == 0){
            if(option==1){
                performSegue(withIdentifier: "1", sender: self)}
            else if(option == 2){
                performSegue(withIdentifier: "t1server", sender: self)
            }
            
        }
        if(indexPath.row == 1){
            performSegue(withIdentifier: "2", sender: self)}
        if(indexPath.row == 2){
            performSegue(withIdentifier: "3", sender: self)}
        
    }

}
