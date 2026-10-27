
#include <iostream>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <cstdlib>
#include <string>
#include <Windows.h>



using namespace sf;
using namespace std;
bool roszadaBialych = false;
bool roszadaCzarnych = false;
bool zamianaCzarnego = false;
bool zamianaBialego = false;
int Azmienianego;
//1 to pionek, 2 to kon, 3 to goniec, 4 to wieza, 5 to hetman, 6 to krol
    class figura
{protected:
     
     bool Czarny = 0;
     
public:
    int identyfikator;
    Sprite obraz;
    Texture tekstura;
    bool pierwszy_ruch = true;
       
    
    figura()
    {   
        pierwszy_ruch = true;
        identyfikator = 0;
        tekstura.loadFromFile("pionek.png");
        obraz.setTexture(tekstura);
        obraz.setOrigin(50.0f, 50.0f);
    }
    int nadanie()
    {
        return identyfikator;
    }
    bool kolor()
    {
        return Czarny;
    }
};


    class pion : public figura
    {
    protected:
        
        
    public:
        pion(bool czyCzarny)
        {
            identyfikator = 1;
            pierwszy_ruch = true;
            if (czyCzarny)
            {
                Czarny = true;
                tekstura.loadFromFile("pionek_czarny.png");
            }
            else { tekstura.loadFromFile("pionek_bialy.png"); Czarny = false; }
            obraz.setTexture(tekstura);
            obraz.setOrigin(50.0f, 50.0f);
            
        }

    };
    
    
    class kon : public figura
    {
    public:
        kon(bool czyCzarny)
        {
            pierwszy_ruch = true;
            identyfikator = 2;
            if (czyCzarny)
            {
                tekstura.loadFromFile("kon_czarny.png");
                Czarny = true;
            }
            else { tekstura.loadFromFile("kon_bialy.png"); Czarny = false; }
            obraz.setTexture(tekstura);
            obraz.setOrigin(50.0f, 50.0f);
        }

    };
    
    
    class goniec :public figura
    {
    public:
        goniec(bool czyCzarny)
        {
            pierwszy_ruch = true;
            identyfikator = 3;
            if (czyCzarny)
            {
                Czarny = true;
                tekstura.loadFromFile("goniec_czarny.png");
            }
            else { tekstura.loadFromFile("goniec_bialy.png"); Czarny = false; }
            obraz.setTexture(tekstura);
            obraz.setOrigin(50.0f, 50.0f);
        }

    };
    
    
    class wieza : public figura
    {
    public:
        wieza(bool czyCzarny)
        {
            pierwszy_ruch = true;
            identyfikator = 4;
            if (czyCzarny)
            {
                Czarny = true;
                tekstura.loadFromFile("wieza_czarny.png");
            }
            else {
                tekstura.loadFromFile("wieza_bialy.png");
                Czarny = false;
            }
            obraz.setTexture(tekstura);
            obraz.setOrigin(50.0f, 50.0f);
        }

    };
    
    
    class hetman : public figura
    {
    public:
        hetman(bool czyCzarny)
        {
            pierwszy_ruch = true;
            identyfikator = 5;
            if (czyCzarny)
            {
                Czarny = true;
                tekstura.loadFromFile("hetman_czarny.png");
            }
            else {
                tekstura.loadFromFile("hetman_bialy.png");
                Czarny = false;
            }
            obraz.setTexture(tekstura);
            obraz.setOrigin(50.0f, 50.0f);
        }

    };
    
    
    class krol : public figura
    {
    public:
        
        krol(bool czyCzarny)
        {
            pierwszy_ruch = true;
            identyfikator = 6;
            if (czyCzarny)
            {
                Czarny = true;
                tekstura.loadFromFile("krol_czarny.png");
            }
            else {
                tekstura.loadFromFile("krol_bialy.png");
                Czarny = false;
            }
            obraz.setTexture(tekstura);
            obraz.setOrigin(50.0f, 50.0f);
        }

    };


    //funkcja rysuje tablice
    bool rysowanie_boarda(RenderWindow& o, Sprite& s, int a, int b, Vector2f& orig)
    {

        float x, y;
        x = (100.0f + (a * 100.0f));
        y = (100.0f + (b * 100.0f));
        s.setPosition(x, y);
        orig = Vector2f(x + 50.0f, y + 50.0f);
        o.draw(s);
        return true;
    }

    //struktura jednego kafelka
    struct szachy
    {
        int ident = 0;
        int a = 0;
        int b = 0;
        Sprite duszek;
        Texture tekstura;
        bool czyZajete = false;
        bool czyCzarny = false;
        Vector2f origin;
        figura postawiony;

    };

    
    




    //funkcja ktora sluzy do przemieszczania pionkow
    bool czyIdzie(int a, int b, int x, int y, int i, bool black, bool& pierwszy, szachy s[8][8])
    {
        int g, h;

        switch (i)
        {
        case 1:


            if (black)
            {
                

                if (a == x)
                {  
                    if (pierwszy)
                    {
                        if (y == b + 1 || y == b + 2)
                        {
                            if (s[a][b + 1].czyZajete) { return false; }
                            else
                            {
                                pierwszy = false;
                                return true;
                            }
                        }
                        else return false;
                    }
                    else
                    {
                        
                        if (y == b + 1)
                        {
                            
                            if (y == 7)
                            {
                                zamianaCzarnego = true;
                                Azmienianego = a;
                             }
                            return true;
                        }
                        else return false;
                    }

                }
                else return false;
            }
            if (!black)
            {
                if (a == x)
                {
                    if (pierwszy)
                    {
                        if (y == b - 1 || y == b - 2)
                        {
                            if (s[a][b - 1].czyZajete) { return false; }
                            else
                            {
                                pierwszy = false;
                                return true;
                            }
                        }
                        else return false;
                    }
                    else
                    {
                        if (y == b - 1)
                        {
                            return true;
                        }
                        else return false;
                    }

                }
                else return false;
            }


            break;

        case 2:
            if (a == x + 2 && b == y + 1) return true;
            else if (a == x + 2 && b == y - 1)return true;
            else if (a == x + 1 && b == y - 2)return true;
            else if (a == x + 1 && b == y + 2)return true;
            else if (a == x - 1 && b == y + 2)return true;
            else if (a == x - 1 && b == y - 2)return true;
            else if (a == x - 2 && b == y + 1)return true;
            else if (a == x - 2 && b == y - 1)return true;
            else return false;
            break;

        case 3:
            a++;
            b++;
            x++;
            y++;
            if (a - x == b - y)
            {
                if (b > y)
                {
                    g = a - 1;
                    h = b - 1;
                    while (h > y && g > x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g--;
                        h--;
                    }
                }
                else if (b < y)
                {
                    g = a + 1;
                    h = b + 1;
                    while (h < y && g < x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g++;
                        h++;
                    }
                }
                else return true;
            }
            else if (a - x == y - b)
            {
                if (a > x)
                {
                    g = a - 1;
                    h = b + 1;
                    while (h < y && g > x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g--;
                        h++;
                    }
                }
                else if (a < x)
                {
                    g = a + 1;
                    h = b - 1;
                    while (h > y && g < x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g++;
                        h--;
                    }
                }
                else return true;
            }
            else return false;
            break;


        case 4:
            a++;
            b++;
            x++;
            y++;
            if (a == x && b != y)
            {
                

                g = a;

                if (b > y)
                {
                    h = b - 1;
                    while (h > y)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        h--;
                    }
                }
                else if (b < y)
                {
                    h = b + 1;
                    while (h < y)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        h++;
                    }

                }
                else return true;
            }
            else if (a != x && b == y)
            {
                h = b;
                if (a > x)
                {
                    g = a - 1;
                    while (g > x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g--;
                    }
                }
                else if (a < x)
                {
                    g = a + 1;
                    while (g < x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g++;
                    }
                }
                else return true;

            }
            else return false;
            break;
        case 5:
         
            a++;
            b++;
            x++;
            y++;
            if (a - x == b - y)
            {
                if (b > y)
                {
                    g = a - 1;
                    h = b - 1;
                    while (h > y && g > x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g--;
                        h--;
                    }
                }
                else if (b < y)
                {
                    g = a + 1;
                    h = b + 1;
                    while (h < y && g < x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g++;
                        h++;
                    }
                }
                else return true;
            }
            else if (a - x == y - b)
            {
                if (a > x)
                {
                    g = a - 1;
                    h = b + 1;
                    while (h < y && g > x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g--;
                        h++;
                    }
                }
                else if (a < x)
                {
                    g = a + 1;
                    h = b - 1;
                    while (h > y && g < x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g++;
                        h--;
                    }
                }
                else return true;
            }
            else if (a == x && b != y)
            {


                g = a;

                if (b > y)
                {
                    h = b - 1;
                    while (h > y)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        h--;
                    }
                }
                else if (b < y)
                {
                    h = b + 1;
                    while (h < y)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        h++;
                    }

                }
                else return true;
            }
            else if (a != x && b == y)
            {
                h = b;
                if (a > x)
                {
                    g = a - 1;
                    while (g > x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g--;
                    }
                }
                else if (a < x)
                {
                    g = a + 1;
                    while (g < x)
                    {
                        if (s[g - 1][h - 1].czyZajete) { return false; }
                        g++;
                    }
                }
                else return true;

            }
            else return false;

            


            break;

        case 6:

            if (pierwszy)
            {
                if (x == a - 2 && y == b)
                {   
                    if (black) { roszadaCzarnych = true; }
                    else { roszadaBialych = true; }
                    pierwszy = false;
                    return true;
                }
                else  if (x == a + 2 && y == b)
                {
                    if (black) { roszadaCzarnych = true; }
                    else { roszadaBialych = true; }
                    pierwszy = false;
                    return true;
                } 
                
            }
            
                if (x == a + 1 && y == b + 1) return true;
                if (x == a + 1 && y == b - 1) return true;
                if (x == a + 1 && y == b) return true;
                if (x == a && y == b + 1) return true;
                if (x == a && y == b - 1) return true;
                if (x == a - 1 && y == b + 1) return true;
                if (x == a - 1 && y == b - 1) return true;
                if (x == a - 1 && y == b) return true;

            


            else return false;
            
        }


    }


    //funkcja sprawdza na ktorym polu znajduje sie mysz
    int oblicz_pozycje_x(Vector2i m, RenderWindow& o)
    {
        m = Mouse::getPosition(o);
        int i = 0;

        while (i < 8)
        {
            if ((m.x - 100 - i * 100) < 100)
            {
                break;

            }
            i++;
        }
        return i;

    }



    //funkcja sprawdza na ktorym polu znajduje sie mysz
    int oblicz_pozycje_y(Vector2i m, RenderWindow& o)
    {
        m = Mouse::getPosition(o);


        int j = 0;
        while (j < 8)
        {
            if ((m.y - 100 - j * 100) < 100)
            {
                break;

            }
            j++;
        }
        return j;

    }



    //funkcja ktora na starcie stawia figure na danym polu
    void ustaw_figure(szachy &s, figura &f)
    {
        s.ident = f.nadanie();
        s.czyCzarny = f.kolor();
        s.postawiony = f;
        s.postawiony.obraz.setPosition(s.origin);
        s.czyZajete = true;        
        
    }



    //funkcja ktora przestawia figure z pola na pole (s1 to ta z ktorej przestawiamy, s2 to ta na ktora stawiamy)
    void przestaw_figure(szachy& ab, szachy& xy , figura &sphol)
    {
        
        ab.postawiony.obraz.setPosition(xy.origin);
        xy.postawiony = ab.postawiony;
        xy.czyZajete = true;
        xy.ident = ab.ident;
        xy.czyCzarny = ab.czyCzarny;
        ab.ident = 0;
        ab.postawiony = sphol;
        ab.czyZajete = false;
        xy.postawiony.pierwszy_ruch = false;
    }


    //funkcja sprawdza czy jest bicie. jeśli jest to jakaś inna figura niż pionek, wykonuje po prostu funkcje czyIdzie
    bool czyBicie(int ide, int a, int b, int x, int y,  bool black, bool& pierwszy, szachy s[8][8], bool abCol, bool xyCol)
    {
        
        if (abCol == xyCol) { return false; }
        else
        {
            if (ide == 1)
            {
                
                if (black)
                {
                    if ((a == x - 1 || a == x + 1) && y == b + 1)
                    {
                        if (y == 7)
                        {
                            zamianaCzarnego = true;
                            Azmienianego = x;
                        }

                        return true;
                    }
                    else return false;
                }
                else
                {
                    if ((a == x - 1 || a == x + 1) && y == b - 1) return true;
                    else return false;
                }
            }
            else if (ide != 1)
            {
                if (czyIdzie(a, b, x, y, ide, black, pierwszy, s)) return true;
            }
            
        }
    }

    bool czySzach(szachy s[8][8], bool CzyRuchCzarnych)
    {   
        int Ba, Bb, Ca, Cb;
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                if (s[i][j].ident == 6)
                {
                    if (s[i][j].czyCzarny)
                    {
                        Ca = s[i][j].a;
                        Cb = s[i][j].b;
                    }
                    else
                    {
                        Ba = s[i][j].a;
                        Bb = s[i][j].b;
                    }
                }
            }
        }
      

        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                
                    if (s[i][j].czyCzarny == true)
                    {
                        if (s[i][j].czyZajete)
                        {
                            if (s[i][j].ident != 1)
                            {
                                
                                if (czyIdzie(s[i][j].a, s[i][j].b, Ba, Bb, s[i][j].ident, s[i][j].czyCzarny, s[i][j].postawiony.pierwszy_ruch, s))
                                {

                                    
                                    if (CzyRuchCzarnych)
                                    {
                                        return true;
                                    }

                                }
                            }
                            if (czyBicie(s[i][j].ident, s[i][j].a, s[i][j].b, Ba, Bb, s[i][j].czyCzarny, s[i][j].postawiony.pierwszy_ruch, s, s[i][j].czyCzarny, s[Ba][Bb].czyCzarny))
                            {
                                
                                if (CzyRuchCzarnych)
                                {
                                    return true;
                                }
                            }
                        }
                        
                    }
                    else if (s[i][j].czyCzarny == false)
                    {
                        if (s[i][j].czyZajete)
                        {   
                            if (s[i][j].ident != 1)
                            {
                                if (czyIdzie(s[i][j].a, s[i][j].b, Ca, Cb, s[i][j].ident, s[i][j].czyCzarny, s[i][j].postawiony.pierwszy_ruch, s))
                                {
                                   
                                    if (!CzyRuchCzarnych)
                                    {
                                        return true;
                                    }
                                }
                            }
                            if (czyBicie(s[i][j].ident, s[i][j].a, s[i][j].b, Ca, Cb, s[i][j].czyCzarny, s[i][j].postawiony.pierwszy_ruch, s, s[i][j].czyCzarny, s[Ca][Cb].czyCzarny))
                            {
                                
                                if (!CzyRuchCzarnych)
                                {
                                    return true;
                                }
                            }
                        }
                        
                    }
                
            }
        }
        return false;
       
    }


    




    int main()
    {
        Sprite poddaj;
        Texture poddajSie;
        poddajSie.loadFromFile("poddaj.png");
        poddaj.setTexture(poddajSie);
        poddaj.setOrigin(100, 50);
        poddaj.setPosition(1200, 150);
        Image wygrana;
        
        Sprite remis;
        Texture rem;
        rem.loadFromFile("remis.png");
        remis.setTexture(rem);
        remis.setOrigin(100, 50);
        remis.setPosition(1200, 350);




        int x = 0;
        int y = 0;
        int a = 0;
        int b = 0;

        Texture pusta;
        pusta.create(100, 100);
        figura spaceHoalder[8][8];
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                spaceHoalder[i][j].obraz.setOrigin(50.0f, 50.0f);
                spaceHoalder[i][j].obraz.setTexture(pusta);
            }
        }


        szachy szachownica[8][8];
        bool ruchCzarnych = false;
        bool na_planszy = true;
        bool czarny = true;
        bool bialy = false;
        pion b_pionek_1(bialy);
        pion b_pionek_2(bialy);
        pion b_pionek_3(bialy);
        pion b_pionek_4(bialy);
        pion b_pionek_5(bialy);
        pion b_pionek_6(bialy);
        pion b_pionek_7(bialy);
        pion b_pionek_8(bialy);
        wieza b_wieza_1(bialy);
        wieza b_wieza_2(bialy);
        kon b_kon_1(bialy);
        kon b_kon_2(bialy);
        goniec b_goniec_1(bialy);
        goniec b_goniec_2(bialy);
        hetman b_hetman(bialy);
        krol b_krol(bialy);

        pion c_pionek_1(czarny);
        pion c_pionek_2(czarny);
        pion c_pionek_3(czarny);
        pion c_pionek_4(czarny);
        pion c_pionek_5(czarny);
        pion c_pionek_6(czarny);
        pion c_pionek_7(czarny);
        pion c_pionek_8(czarny);
        wieza c_wieza_1(czarny);
        wieza c_wieza_2(czarny);
        kon c_kon_1(czarny);
        kon c_kon_2(czarny);
        goniec c_goniec_1(czarny);
        goniec c_goniec_2(czarny);
        hetman c_hetman(czarny);
        krol c_krol(czarny);

        figura bufor;





        //nadawanie tekstur każdemu kafelkowi szachownicy
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 8; j++)
            {

                if ((i + 2) % 2 == 1 && (j + 2) % 2 == 0 || (i + 2) % 2 == 0 && (j + 2) % 2 == 1)
                {
                    szachownica[i][j].tekstura.loadFromFile("czarne.png");
                    szachownica[i][j].duszek.setTexture(szachownica[i][j].tekstura);
                }
                else
                {
                    szachownica[i][j].tekstura.loadFromFile("biale.png");
                    szachownica[i][j].duszek.setTexture(szachownica[i][j].tekstura);
                }


            }
        }





        RenderWindow okno(VideoMode(1700, 1000), "szachy");
        Event wydarzenie;
        View widok;
        widok.reset(FloatRect(0, 0, 1700, 1000));
        okno.setView(widok);


        //rysowanie szachownicy po raz pierwszy dla zainicjowania wartości
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 8; j++)
            {

                rysowanie_boarda(okno, szachownica[i][j].duszek, i, j, szachownica[i][j].origin);
                szachownica[i][j].a = i;
                szachownica[i][j].b = j;

            }
        }

        ustaw_figure(szachownica[0][0], c_wieza_1);
        ustaw_figure(szachownica[1][0], c_kon_1);
        ustaw_figure(szachownica[2][0], c_goniec_1);
        ustaw_figure(szachownica[3][0], c_hetman);
        ustaw_figure(szachownica[4][0], c_krol);
        ustaw_figure(szachownica[5][0], c_goniec_2);
        ustaw_figure(szachownica[6][0], c_kon_2);
        ustaw_figure(szachownica[7][0], c_wieza_2);
        ustaw_figure(szachownica[0][1], c_pionek_1);
        ustaw_figure(szachownica[1][1], c_pionek_2);
        ustaw_figure(szachownica[2][1], c_pionek_3);
        ustaw_figure(szachownica[3][1], c_pionek_4);
        ustaw_figure(szachownica[4][1], c_pionek_5);
        ustaw_figure(szachownica[5][1], c_pionek_6);
        ustaw_figure(szachownica[6][1], c_pionek_7);
        ustaw_figure(szachownica[7][1], c_pionek_8);

        ustaw_figure(szachownica[0][7], b_wieza_1);
        ustaw_figure(szachownica[1][7], b_kon_1);
        ustaw_figure(szachownica[2][7], b_goniec_1);
        ustaw_figure(szachownica[3][7], b_hetman);
        ustaw_figure(szachownica[4][7], b_krol);
        ustaw_figure(szachownica[5][7], b_goniec_2);
        ustaw_figure(szachownica[6][7], b_kon_2);
        ustaw_figure(szachownica[7][7], b_wieza_2);
        ustaw_figure(szachownica[0][6], b_pionek_1);
        ustaw_figure(szachownica[1][6], b_pionek_2);
        ustaw_figure(szachownica[2][6], b_pionek_3);
        ustaw_figure(szachownica[3][6], b_pionek_4);
        ustaw_figure(szachownica[4][6], b_pionek_5);
        ustaw_figure(szachownica[5][6], b_pionek_6);
        ustaw_figure(szachownica[6][6], b_pionek_7);
        ustaw_figure(szachownica[7][6], b_pionek_8);



        while (okno.isOpen())
        {

            Vector2i mysz = Mouse::getPosition(okno);
            x = oblicz_pozycje_x(mysz, okno);
            y = oblicz_pozycje_y(mysz, okno);
            okno.clear(Color::Blue);



            // narysowanie całej szachownicy na ekranie
            for (int i = 0; i < 8; i++)
            {
                for (int j = 0; j < 8; j++)
                {

                    rysowanie_boarda(okno, szachownica[i][j].duszek, i, j, szachownica[i][j].origin);
                    szachownica[i][j].a = i;
                    szachownica[i][j].b = j;
                }
            }
            okno.draw(poddaj);
            okno.draw(remis);

            if (na_planszy == false)
            {
                szachownica[a][b].postawiony.obraz.setPosition(float(mysz.x), float(mysz.y));
            }


            if (mysz.x > 100 && mysz.x < 900 && mysz.y >100 && mysz.y < 900)
            {

                if (Mouse::isButtonPressed(Mouse::Left))
                {
                    if (szachownica[x][y].postawiony.obraz.getGlobalBounds().contains(okno.mapPixelToCoords(mysz)) && na_planszy == true)
                    {
                        a = x;
                        b = y;
                        na_planszy = false;

                    }
                    else if (na_planszy == false)
                    {
                        if (mysz.x > 100 && mysz.x < 900 && mysz.y >100 && mysz.y < 900)
                        {

                            if (szachownica[x][y].czyZajete == true)
                            {
                                if (czyBicie(szachownica[a][b].ident, a, b, x, y, szachownica[a][b].czyCzarny, szachownica[a][b].postawiony.pierwszy_ruch, szachownica, szachownica[a][b].czyCzarny, szachownica[x][y].czyCzarny))
                                {
                                    if (ruchCzarnych == szachownica[a][b].postawiony.kolor())
                                    {
                                        bufor = szachownica[x][y].postawiony;
                                        przestaw_figure(szachownica[a][b], szachownica[x][y], spaceHoalder[a][b]);
                                        ruchCzarnych = !ruchCzarnych;

                                        if (zamianaCzarnego == true)
                                        {
                                            int w;
                                            cout << " w co zamieniasz " << endl;
                                            cin >> w;
                                            switch (w)
                                            {
                                            case 1:
                                                ustaw_figure(szachownica[Azmienianego][7], c_kon_1);
                                                break;
                                            case 2:
                                                ustaw_figure(szachownica[Azmienianego][7], c_goniec_1);
                                                break;
                                            case 3:
                                                ustaw_figure(szachownica[Azmienianego][7], c_wieza_1);
                                                break;
                                            case 4:
                                                ustaw_figure(szachownica[Azmienianego][7], c_hetman);
                                                break;
                                            }
                                            zamianaCzarnego = false;
                                        }
                                        if (zamianaBialego == true)
                                        {   
                                            int w;
                                            cout << " w co zamieniasz " << endl;
                                            cin >> w;
                                            switch (w)
                                            {
                                            case 1:
                                                ustaw_figure(szachownica[Azmienianego][7], b_kon_1);
                                                break;
                                            case 2:
                                                ustaw_figure(szachownica[Azmienianego][7], b_goniec_1);
                                                break;
                                            case 3:
                                                ustaw_figure(szachownica[Azmienianego][7], b_wieza_1);
                                                break;
                                            case 4:
                                                ustaw_figure(szachownica[Azmienianego][7], b_hetman);
                                                break;
                                            }
                                            zamianaBialego = false;
                                        }

                                        if (czySzach(szachownica, ruchCzarnych))
                                        {
                                            przestaw_figure(szachownica[x][y], szachownica[a][b], bufor);
                                            szachownica[a][b].postawiony.pierwszy_ruch = true;
                                            ruchCzarnych = !ruchCzarnych;
                                           
                                        }

                                    }
                                }
                                else
                                {
                                    szachownica[a][b].postawiony.obraz.setPosition(szachownica[a][b].origin);
                                }
                            }
                            else
                            {
                                if (x == a && y == b)
                                {
                                    szachownica[a][b].postawiony.obraz.setPosition(szachownica[a][b].origin);
                                }
                                if (ruchCzarnych != szachownica[a][b].postawiony.kolor())
                                {
                                    szachownica[a][b].postawiony.obraz.setPosition(szachownica[a][b].origin);
                                }
                                else
                                {
                                    if (czyIdzie(a, b, x, y, szachownica[a][b].ident, szachownica[a][b].czyCzarny, szachownica[a][b].postawiony.pierwszy_ruch, szachownica))
                                    {
                                        if (ruchCzarnych == szachownica[a][b].postawiony.kolor())
                                        {
                                            przestaw_figure(szachownica[a][b], szachownica[x][y], spaceHoalder[a][b]);
                                            ruchCzarnych = !ruchCzarnych;
                                            if (zamianaCzarnego == true)
                                            {
                                                int w;
                                                cout << " w co zamieniasz " << endl;
                                                cin >> w;
                                                switch (w)
                                                {
                                                case 1:
                                                    ustaw_figure(szachownica[Azmienianego][7], c_kon_1);
                                                    break;
                                                case 2:
                                                    ustaw_figure(szachownica[Azmienianego][7], c_goniec_1);
                                                    break;
                                                case 3:
                                                    ustaw_figure(szachownica[Azmienianego][7], c_wieza_1);
                                                    break;
                                                case 4:
                                                    ustaw_figure(szachownica[Azmienianego][7], c_hetman);
                                                    break;
                                                }
                                                
                                                
                                                zamianaCzarnego = false;
                                            }
                                            if (zamianaBialego == true)
                                            {
                                                int w;
                                                cout << " w co zamieniasz " << endl;
                                                cin >> w;
                                                switch (w)
                                                {
                                                case 1:
                                                    ustaw_figure(szachownica[Azmienianego][7], b_kon_1);
                                                    break;
                                                case 2:
                                                    ustaw_figure(szachownica[Azmienianego][7], b_goniec_1);
                                                    break;
                                                case 3:
                                                    ustaw_figure(szachownica[Azmienianego][7], b_wieza_1);
                                                    break;
                                                case 4:
                                                    ustaw_figure(szachownica[Azmienianego][7], b_hetman);
                                                    break;
                                                }
                                                zamianaBialego = false;
                                            }


                                            if (czySzach(szachownica, ruchCzarnych))
                                            {
                                                przestaw_figure(szachownica[x][y], szachownica[a][b], spaceHoalder[x][y]);
                                                szachownica[a][b].postawiony.pierwszy_ruch = true;
                                                ruchCzarnych = !ruchCzarnych;
                                            }
                                            if (roszadaCzarnych == true)
                                            {
                                                if (szachownica[2][0].postawiony.identyfikator == 6)
                                                {
                                                    przestaw_figure(szachownica[0][0], szachownica[3][0], spaceHoalder[0][0]);
                                                }
                                                else if (szachownica[6][0].postawiony.identyfikator == 6)
                                                {
                                                    przestaw_figure(szachownica[7][0], szachownica[5][0], spaceHoalder[7][0]);
                                                }
                                                roszadaCzarnych = false;
                                            }
                                            if (roszadaBialych)
                                            {
                                                
                                                if (szachownica[2][7].postawiony.identyfikator == 6)
                                                {
                                                    przestaw_figure(szachownica[0][7], szachownica[3][7], spaceHoalder[0][7]);
                                                }
                                                else if (szachownica[6][7].postawiony.identyfikator == 6)
                                                {
                                                    przestaw_figure(szachownica[7][7], szachownica[5][7], spaceHoalder[7][7]);
                                                }
                                                roszadaBialych = false;
                                            }

                                        }
                                    }
                                    else
                                    {

                                        szachownica[a][b].postawiony.obraz.setPosition(szachownica[a][b].origin);
                                    }

                                }
                            }

                            na_planszy = true;
                        }
                    }

                    

                    
                    while (Mouse::isButtonPressed(Mouse::Left)) {}
                }
            }

            if (Mouse::isButtonPressed(Mouse::Left))
            {   
                
                if (poddaj.getGlobalBounds().contains(okno.mapPixelToCoords(mysz)) && na_planszy == true)
                {
                    Sprite d;
                    Texture t;
                    
                    if (ruchCzarnych == false)
                    { 
                        wygrana.loadFromFile("w_czar.png");
                        okno.clear(Color::Black); 
                        
                        t.loadFromImage(wygrana);
                        d.setTexture(t);
                        okno.draw(d);
                        okno.display(); 
                        Sleep(5000); 
                        break; 
                    }
                    else
                    {
                        wygrana.loadFromFile("w_bial.png");
                        okno.clear(Color::White);
                        t.loadFromImage(wygrana);
                        d.setTexture(t);
                        okno.draw(d);
                        okno.display();
                        Sleep(5000);
                        break;
                    }

                   
                }
                if (remis.getGlobalBounds().contains(okno.mapPixelToCoords(mysz)) && na_planszy == true)
                {
                    Sprite d;
                    Texture t;
                    wygrana.loadFromFile("rem.png");
                    okno.clear(Color::Black);
                    t.loadFromImage(wygrana);
                    d.setTexture(t);
                    okno.draw(d);
                    okno.display();
                    Sleep(5000);
                    break;

                }




                while (Mouse::isButtonPressed(Mouse::Left)) {}

            }


            for (int i = 0; i < 8; i++)
            {
                for (int j = 0; j < 8; j++)
                {

                    okno.draw(szachownica[i][j].postawiony.obraz);
                }
            }

            while (okno.pollEvent(wydarzenie))
            {
                if (wydarzenie.type == Event::Resized)
                {
                    okno.setView(View({ 0,0, float(wydarzenie.size.width), float(wydarzenie.size.height) }));
                }
                if (wydarzenie.type == Event::Closed) { okno.close(); }

            }

            okno.display();


        }
        return 0;

    }