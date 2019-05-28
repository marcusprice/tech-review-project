from django.test import TestCase
from .models import TechType, Product, Review
from .views import index, gettypes, getproducts, newProduct
from .forms import TechTypeForm
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class TechTypeTest(TestCase):
    def test_string(self):
       type=TechType(techtypename="Tablet")
       self.assertEqual(str(type), type.techtypename)

    def test_table(self):
       self.assertEqual(str(TechType._meta.db_table), 'techtype')

class ProductTest(TestCase):
    #set up one time sample data
    def setup(self):
       type = TechType(techtypename='laptop')
       product=Product(productname='Lenovo', techtype=type, productprice='500.00')
       return product

    def test_string(self):
       prod = self.setup()
       self.assertEqual(str(prod), prod.productname)

    #test the discount property
    def test_discount(self):
       prod=self.setup()
       self.assertEqual(prod.memberDiscount(), 25.00)

    def test_type(self):
       prod=self.setup()
       self.assertEqual(str(prod.techtype), 'laptop')

    def test_table(self):
       self.assertEqual(str(Product._meta.db_table), 'product')

class ReviewTest(TestCase):
    def test_string(self):
       rev=Review(reviewtitle="Best Review")
       self.assertEqual(str(rev), rev.reviewtitle)

    def test_table(self):
       self.assertEqual(str(Review._meta.db_table), 'review')

class IndexTest(TestCase):
    def test_view_url_accessible_by_name(self):
       response = self.client.get(reverse('index'))
       self.assertEqual(response.status_code, 200)

class GetProductsTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.u=User.objects.create(username='myuser')
        self.type=TechType.objects.create(techtypename='laptop')
        self.prod = Product.objects.create(productname='product1', techtype=self.type, user=self.u, productprice=500, productentrydate='2019-04-02', productdescription="a product")
        self.rev1=Review.objects.create(reviewtitle='prodreview', reviewdate='2019-04-03', product=self.prod, rating=4, reviewtext='some review')
        self.rev1.user.add(self.u)
        self.rev2=Review.objects.create(reviewtitle='prodreview', reviewdate='2019-04-03', product=self.prod,  rating=4, reviewtext='some review')
        self.rev2.user.add(self.u)

    def test_product_detail_success(self):
        response = self.client.get(reverse('productdetails', args=(self.prod.id,)))
        # Assert that self.post is actually returned by the post_detail view
        self.assertEqual(response.status_code, 200)

    def test_discount(self):
        discount=self.prod.memberDiscount()
        self.assertEqual(discount, 25.00)

    def test_number_of_reviews(self):
        reviews=Review.objects.filter(product=self.prod).count()
        self.assertEqual(reviews, 2)

#Form tests
class TechType_Form_Test(TestCase):
    def test_typeform_is_valid(self):
        form=TechTypeForm(data={'techtypename': "type1", 'techtypedescription' : "some type"})
        self.assertTrue(form.is_valid())

    def test_typeform_minus_descript(self):
        form=TechTypeForm(data={'techtypename': "type1"})
        self.assertTrue(form.is_valid())

    def test_typeform_empty(self):
        form=TechTypeForm(data={'techtypename': ""})
        self.assertFalse(form.is_valid())

class New_Product_authentication_test(TestCase):
    def setUp(self):
        self.test_user=User.objects.create_user(username='testuser1', password='P@ssw0rd1')
        self.type=TechType.objects.create(techtypename='laptop')

    def test_redirect_if_not_logged_in(self):
        response=self.client.get(reverse('newproduct'))
        self.assertRedirects(response, '/accounts/login/?next=/techapp/newProduct/')

    def test_Logged_in_uses_correct_template(self):
        login=self.client.login(username='testuser1', password='P@ssw0rd1')
        response=self.client.get(reverse('newproduct'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'techapp/newproduct.html')
