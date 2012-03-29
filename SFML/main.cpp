
////////////////////////////////////////////////////////////
// Headers
////////////////////////////////////////////////////////////
#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>
#include <stdio.h>
///////
// Model
///////
class Model
{
public:
    // constructor/destructor
    Model(){}
    void initializeFromDimensions(int Xn, int Yn){
        this->Xn = Xn;
        this->Yn = Yn;
        map = new char*[Xn];
        for (int x = 0; x < Xn; x++){
            map[x] = new char[Yn];
            for (int y = 0; y < Yn; y++){
                map[x][y] = 0;
            }
        }
    }
    static Model fromDimensions(int Xn, int Yn){ return Model(Xn,Yn); }
    Model(int Xn, int Yn){
        this->Xn = Xn;
        this->Yn = Yn;
        map = new char*[Xn];
        for (int x = 0; x < Xn; x++){
            map[x] = new char[Yn];
            for (int y = 0; y < Yn; y++){
                map[x][y] = 0;
            }
        }
    }
    ~Model(){
        for (int x = 0; x < Xn; x++){
            delete [] map[x];
        }
        delete [] map;
    }
    
    // reset map
    void reset(){
        for (int x = 0; x < Xn; x++){
            for (int y = 0; y < Yn; y++){
                map[x][y] = 0;
            }
        }
    }
    
    // draw an X across the board
    void drawX(){
        int smaller = Xn < Yn ? Xn : Yn;
        for (int x = 0; x < smaller; x++){
            this->toggle(x,x);
            this->toggle(smaller-1-x,x);
        }
    }
    
    // tick per Conway's game of life.
    void tick(){
        char** newMap = new char*[Xn];
        for (int x = 0; x < Xn; x++){
            newMap[x] = new char[Yn];
            for (int y = 0; y < Yn; y++){
                switch (countNeighbors(x,y)){
                    case 0:
                    case 1:
                    case 4:
                    case 5:
                    case 6:
                    case 7:
                    case 8:
                        newMap[x][y] = 0;
                        break;
                    case 2:
                        newMap[x][y] = map[x][y];
                        break;
                    case 3:
                        newMap[x][y] = 1;
                        break;
                }
            }
        }
        
        // Now replace the current map with newMap
        for (int x = 0; x < Xn; x++){
            delete [] map[x];
        }
        delete [] map;
        map = newMap;
    }
    
    // get map and dimensions
    char** getMap(){ return map; }
    int getXn() { return Xn; }
    int getYn() { return Yn; }
    // toggle etc.
    void toggle(int x, int y){
        if (map[x][y] == 0){
            map[x][y] = 1;
        }
        else if (map[x][y] == 1){
            map[x][y] = 0;
        }
        else {
            map[x][y] = 2;
        }
    }
//private:
    char** map;
    int Xn, Yn;
    
    // Helper methods for tick
    int countNeighbors(int x, int y){
        int ret = 0;
        int dd[] = { -1, 0, 1};
        int currentX, currentY;
        for (int xi = 0; xi < 3; xi++){
            currentX = x + dd[xi];
            if (currentX < 0) currentX += Xn;
            else if (currentX >= Xn) currentX -= Xn;
            
            for (int yi = 0; yi < 3; yi++){
                currentY = y + dd[yi];
                if (currentY < 0) currentY += Yn;
                else if (currentY >= Yn) currentY -= Yn;
                
                if (map[currentX][currentY] == 1) ret++;
            }
        }
        
        if (map[x][y] == 1) ret -= 1;
        
        return ret;
    }
};

/////////
// View
/////////
class View
{
public:
    View(sf::RenderWindow* App, int xpixels, int ypixels){this->App = App; this->xpixels = xpixels; this->ypixels = ypixels; AppIsDynamicallyAllocated = false;}
    View(int xpixels, int ypixels, char* title){
        App = new sf::RenderWindow;
        App->Create(sf::VideoMode(xpixels,ypixels), title);
    }
    ~View(){
        if (AppIsDynamicallyAllocated){
            delete App;
        }
    }
    
    // Cleanup.
    bool isOpen(){
        return App->IsOpened();
    }
    void close(){
        App->Close();
    }
    
    // Input.
    bool getEvent(sf::Event& event){
        return App->GetEvent(event);
    }
    void getMouseSquare(int Xn, int Yn, int& x, int& y){
        const sf::Input& input = App->GetInput();
        unsigned int mouseX = input.GetMouseX();
        unsigned int mouseY = input.GetMouseY();
        x = (mouseX * Xn) / xpixels;
        y = (mouseY * Yn) / ypixels;
    }
    
    // Drawing method.
    void draw(int Xn, int Yn, char** map){
        this->App->Clear();
        this->drawGridOutline(Xn,Yn);
        this->drawMap(Xn,Yn,map);
        
        //char buf[10];
        //sprintf(buf, "%d",count);
        //App->Draw(sf::String(buf));
        this->App->Display();
    }
    
private:
    sf::RenderWindow* App;
    sf::Event event;
    int xpixels, ypixels;
    bool AppIsDynamicallyAllocated;
    
    // Draw helper methods.
    void drawGridOutline(int Xn, int Yn){
        for (int i = 0; i < Xn; i++){
            this->App->Draw(sf::Shape::Line( (i*xpixels)/Xn, 0, (i *ypixels)/Xn, 640, 1.0, sf::Color(0,128,0)));
        }
        for (int i = 0; i < Yn; i++){
            this->App->Draw(sf::Shape::Line(0, (i*xpixels)/Yn, 640, (i*ypixels)/Yn, 1.0, sf::Color(0,128,0)));
        }
    }
    void drawMap(int Xn, int Yn, char** map){
        for (int x = 0; x < Xn; x++){
            for (int y = 0; y < Yn; y++){
                if (map[x][y] == 1){
                    App->Draw(sf::Shape::Rectangle((x*xpixels)/Xn, (y*ypixels)/Yn, ((x+1)*xpixels)/Xn, ((y+1)*ypixels)/Yn, sf::Color(0,0,128)));
                }
            }
        }
    }

};

////////////////////////////////////////////////////////////
/// controller 
////////////////////////////////////////////////////////////
class Controller{
public:
    void initialize(Model* model, View* view)
    {
        this->model = model;
        this->view = view;
    }
    
    void runLoop()
    {
        while (view->isOpen()){
            draw();
            processEvents();
        }
    }
    
    void draw(){
        view->draw(model->getXn(),model->getYn(),model->getMap());
    }
    
    void processEvents(){
        sf::Event event;
        while (view->getEvent(event))
        {
            // Close window : exit
            if (event.Type == sf::Event::Closed)
                view->close();
            // Text
            else if (event.Type == sf::Event::KeyPressed)
            {
                if (event.Key.Code == 'q'){
                    view->close();
                }
                // tick the game of life
                else if (event.Key.Code == 't'){
                    model->tick();
                }
                // Reset the board
                else if (event.Key.Code == 'r'){
                    model->reset();
                }
                // Draw an X
                else if (event.Key.Code == 'x'){
                    model->drawX();
                }
            }
            // mouse click
            else if (event.Type == sf::Event::MouseButtonPressed)
            {
                int x, y;
                view->getMouseSquare(model->getXn(), model->getYn(), x,y);
                model->toggle(x, y);
            }
        }

    }
private:
    View* view;
    Model* model;
    bool viewIsDynamicallyAllocated;
    bool modelIsDynamicallyAllocated;
};


////////////////////////////////////////////////////////////
/// Entry point of application
///
/// \return Application exit code
///
////////////////////////////////////////////////////////////

int main()
{
    // Create main window
    // sf::RenderWindow App(sf::VideoMode(640, 480), "SFML Graphics", sf::Style::Fullscreen);
    sf::RenderWindow App(sf::VideoMode(640, 640), "SFML Graphics");
    View view(&App, 640, 640);
    // View view(640, 640, "Hello world");
    Model model(20,20);
    
    
    // Start game loop
    while (view.isOpen())
    {
        // Draw the view
        //view.draw(model.getXn(), model.getYn(), model.getMap(), model.countNeighbors(5, 5));
        view.draw(model.getXn(), model.getYn(), model.getMap());
        
        // Process events
        sf::Event event;
        while (view.getEvent(event))
        {
            // Close window : exit
            if (event.Type == sf::Event::Closed)
                view.close();
            // Text
            else if (event.Type == sf::Event::KeyPressed)
            {
                if (event.Key.Code == 'q'){
                    view.close();
                }
                // tick the game of life
                else if (event.Key.Code == 't'){
                    model.tick();
                }
                // Reset the board
                else if (event.Key.Code == 'r'){
                    model.reset();
                }
                // Draw an X
                else if (event.Key.Code == 'x'){
                    model.drawX();
                }
            }
            // mouse click
            else if (event.Type == sf::Event::MouseButtonPressed)
            {
                int x, y;
                view.getMouseSquare(model.getXn(), model.getYn(), x,y);
                model.toggle(x, y);
            }
        }
    }

    return EXIT_SUCCESS;
}
